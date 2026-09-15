# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import http.server
import json
import threading
import time
import unittest
from unittest import mock
import urllib.request
import urllib.error
import sys

class LiteRTOpenAIServerTest(unittest.TestCase):

    def setUp(self):
        # Safely mock litert_lm for this test run only
        self.mock_litert = mock.MagicMock()
        self.patcher = mock.patch.dict(sys.modules, {'litert_lm': self.mock_litert})
        self.patcher.start()

        # Import litert_server after the module is mocked
        from google.antigravity.connections.local import litert_server
        self.litert_server_mod = litert_server

        self.mock_engine = mock.MagicMock()

        # Wait for server to bind port properly
        self.server = litert_server.LiteRTOpenAIServer(
            ("127.0.0.1", 0),
            litert_server.LiteRTOpenAIHandler,
            self.mock_engine,
            "test_model"
        )
        self.port = self.server.server_port

        # Set up event to signal when server is ready
        self.server_ready = threading.Event()

        # We need a custom server run method to set the event
        def serve_and_signal():
            self.server_ready.set()
            self.server.serve_forever()

        self.server_thread = threading.Thread(target=serve_and_signal)
        self.server_thread.daemon = True
        self.server_thread.start()

        # Wait until server reports it's ready, with a small extra delay for safety
        self.server_ready.wait(timeout=2.0)
        time.sleep(0.05)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
        self.patcher.stop()

    def test_handle_error_suppresses_connection_reset(self):
        mock_exc = ConnectionResetError()
        with mock.patch("sys.exc_info", return_value=(None, mock_exc, None)):
            with mock.patch("logging.debug") as mock_debug:
                self.server.handle_error(mock.MagicMock(), ("127.0.0.1", 12345))
                mock_debug.assert_called_with("Client %s disconnected (%s)", ("127.0.0.1", 12345), mock_exc)

    def test_handle_error_does_not_suppress_other_errors(self):
        mock_exc = ValueError()
        with mock.patch("sys.exc_info", return_value=(None, mock_exc, None)):
            with mock.patch("http.server.ThreadingHTTPServer.handle_error") as mock_super:
                mock_request = mock.MagicMock()
                self.server.handle_error(mock_request, ("127.0.0.1", 12345))
                mock_super.assert_called_with(mock_request, ("127.0.0.1", 12345))

    def test_do_get_models(self):
        url = f"http://127.0.0.1:{self.port}/v1/models"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["object"], "list")
            self.assertEqual(len(data["data"]), 1)
            self.assertEqual(data["data"][0]["id"], "test_model")

    def test_do_get_not_found(self):
        url = f"http://127.0.0.1:{self.port}/notfound"
        req = urllib.request.Request(url)
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(cm.exception.code, 404)

    def test_do_post_missing_messages(self):
        url = f"http://127.0.0.1:{self.port}/v1/chat/completions"
        data = json.dumps({}).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(cm.exception.code, 400)

    def test_do_post_invalid_json(self):
        url = f"http://127.0.0.1:{self.port}/v1/chat/completions"
        data = b"{invalid json"
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(cm.exception.code, 400)

    def test_do_post_synchronous(self):
        mock_conv = mock.MagicMock()
        self.mock_engine.create_conversation.return_value.__enter__.return_value = mock_conv

        mock_conv.send_message.return_value = {
            "content": [{"type": "text", "text": "Hello world!"}],
            "tool_calls": []
        }

        url = f"http://127.0.0.1:{self.port}/v1/chat/completions"
        payload = {
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": False
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')

        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            result = json.loads(response.read().decode())
            self.assertEqual(result["model"], "test_model")
            self.assertEqual(result["choices"][0]["message"]["content"], "Hello world!")
            self.assertEqual(result["choices"][0]["finish_reason"], "stop")

    def test_do_post_streaming(self):
        mock_conv = mock.MagicMock()
        self.mock_engine.create_conversation.return_value.__enter__.return_value = mock_conv

        def stream_generator(prompt):
            yield {"content": [{"type": "text", "text": "Hello "}]}
            yield {"content": [{"type": "text", "text": "world!"}]}

        mock_conv.send_message_async.side_effect = stream_generator

        url = f"http://127.0.0.1:{self.port}/v1/chat/completions"
        payload = {
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')

        # Since it's a Server-Sent Events stream, the connection remains open.
        # We need to read line-by-line or chunk-by-chunk and stop when we see the "DONE" marker.
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)

            full_data = b""
            while True:
                line = response.readline()
                if not line:
                    break
                full_data += line
                if b"data: [DONE]" in line:
                    break

            chunks = full_data.decode().strip().split("\n\n")

            self.assertGreaterEqual(len(chunks), 4)

            self.assertTrue(chunks[0].startswith("data: "))
            chunk1 = json.loads(chunks[0][6:])
            self.assertEqual(chunk1["choices"][0]["delta"]["role"], "assistant")

            chunk2 = json.loads(chunks[1][6:])
            self.assertEqual(chunk2["choices"][0]["delta"]["content"], "Hello ")

            chunk3 = json.loads(chunks[2][6:])
            self.assertEqual(chunk3["choices"][0]["delta"]["content"], "world!")

            self.assertEqual(chunks[-1], "data: [DONE]")

if __name__ == "__main__":
    unittest.main()
