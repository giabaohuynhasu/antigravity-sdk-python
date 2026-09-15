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

"""Tests for models."""

import os
import unittest
from unittest import mock

from google.antigravity import models


class ModelsTest(unittest.TestCase):

  def test_gemini_api_endpoint_validate_base_url(self):
    endpoint = models.GeminiAPIEndpoint(base_url="http://foo")
    # Should not raise
    endpoint.validate_endpoint()

  def test_gemini_api_endpoint_validate_api_key(self):
    endpoint = models.GeminiAPIEndpoint(api_key="secret")
    # Should not raise
    endpoint.validate_endpoint()

  @mock.patch.dict(os.environ, {"GEMINI_API_KEY": "env_secret"}, clear=True)
  def test_gemini_api_endpoint_validate_env_key(self):
    endpoint = models.GeminiAPIEndpoint()
    # Should not raise
    endpoint.validate_endpoint()

  @mock.patch.dict(os.environ, {}, clear=True)
  def test_gemini_api_endpoint_validate_raises(self):
    endpoint = models.GeminiAPIEndpoint()
    with self.assertRaisesRegex(ValueError, "A Gemini API key is required"):
      endpoint.validate_endpoint()

  def test_vertex_endpoint_validate_base_url(self):
    endpoint = models.VertexEndpoint(base_url="http://foo")
    # Should not raise
    endpoint.validate_endpoint()

  def test_vertex_endpoint_validate_api_key(self):
    endpoint = models.VertexEndpoint(api_key="secret")
    # Should not raise
    endpoint.validate_endpoint()

  def test_vertex_endpoint_validate_project_location(self):
    endpoint = models.VertexEndpoint(project="p", location="l")
    # Should not raise
    endpoint.validate_endpoint()

  def test_vertex_endpoint_validate_both_raises(self):
    endpoint = models.VertexEndpoint(project="p", api_key="secret")
    with self.assertRaisesRegex(ValueError, "Cannot specify both"):
      endpoint.validate_endpoint()

    endpoint = models.VertexEndpoint(location="l", api_key="secret")
    with self.assertRaisesRegex(ValueError, "Cannot specify both"):
      endpoint.validate_endpoint()

  @mock.patch.dict(os.environ, {}, clear=True)
  def test_vertex_endpoint_validate_neither_raises(self):
    endpoint = models.VertexEndpoint()
    with self.assertRaisesRegex(ValueError, "either \\(project and location\\) or api_key must be set"):
      endpoint.validate_endpoint()

    endpoint = models.VertexEndpoint(project="p")
    with self.assertRaisesRegex(ValueError, "either \\(project and location\\) or api_key must be set"):
      endpoint.validate_endpoint()

    endpoint = models.VertexEndpoint(location="l")
    with self.assertRaisesRegex(ValueError, "either \\(project and location\\) or api_key must be set"):
      endpoint.validate_endpoint()

  @mock.patch.dict(
      os.environ,
      {"GOOGLE_CLOUD_PROJECT": "env_p", "GOOGLE_CLOUD_LOCATION": "env_l"},
      clear=True,
  )
  def test_vertex_endpoint_populate_env_vars(self):
    endpoint = models.VertexEndpoint()
    self.assertEqual(endpoint.project, "env_p")
    self.assertEqual(endpoint.location, "env_l")
    # Should not raise
    endpoint.validate_endpoint()

  @mock.patch.dict(
      os.environ,
      {"GOOGLE_CLOUD_PROJECT": "env_p", "GOOGLE_CLOUD_LOCATION": "env_l"},
      clear=True,
  )
  def test_vertex_endpoint_no_populate_if_base_url(self):
    endpoint = models.VertexEndpoint(base_url="http://foo")
    self.assertIsNone(endpoint.project)
    self.assertIsNone(endpoint.location)

  @mock.patch.dict(
      os.environ,
      {"GOOGLE_CLOUD_PROJECT": "env_p", "GOOGLE_CLOUD_LOCATION": "env_l"},
      clear=True,
  )
  def test_vertex_endpoint_no_populate_if_api_key(self):
    endpoint = models.VertexEndpoint(api_key="secret")
    self.assertIsNone(endpoint.project)
    self.assertIsNone(endpoint.location)

  def test_model_target_defaults(self):
    target = models.ModelTarget()
    self.assertEqual(target.types, [models.ModelType.TEXT])
    self.assertIsNone(target.name)
    self.assertIsNone(target.endpoint)


if __name__ == "__main__":
  unittest.main()
