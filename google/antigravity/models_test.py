import os
import unittest.mock
import pytest

from google.antigravity import models

def test_gemini_endpoint_base_url():
    """Test validation succeeds when base_url is set."""
    endpoint = models.GeminiAPIEndpoint(base_url="https://example.com")
    endpoint.validate_endpoint()  # Should not raise


def test_gemini_endpoint_api_key():
    """Test validation succeeds when api_key is provided."""
    endpoint = models.GeminiAPIEndpoint(api_key="secret")
    endpoint.validate_endpoint()  # Should not raise


def test_gemini_endpoint_env_var():
    """Test validation succeeds when GEMINI_API_KEY env var is set."""
    with unittest.mock.patch.dict(os.environ, {"GEMINI_API_KEY": "secret"}):
        endpoint = models.GeminiAPIEndpoint()
        endpoint.validate_endpoint()  # Should not raise


def test_gemini_endpoint_missing_auth():
    """Test validation fails when no auth or base_url is provided."""
    # Ensure GEMINI_API_KEY is not in the environment
    env_copy = os.environ.copy()
    env_copy.pop("GEMINI_API_KEY", None)
    with unittest.mock.patch.dict(os.environ, env_copy, clear=True):
        endpoint = models.GeminiAPIEndpoint()
        with pytest.raises(ValueError, match="A Gemini API key is required"):
            endpoint.validate_endpoint()


def test_vertex_endpoint_env_vars_population():
    """Test project and location are populated from env vars."""
    with unittest.mock.patch.dict(
        os.environ,
        {"GOOGLE_CLOUD_PROJECT": "env-project", "GOOGLE_CLOUD_LOCATION": "env-location"}
    ):
        endpoint = models.VertexEndpoint()
        assert endpoint.project == "env-project"
        assert endpoint.location == "env-location"


def test_vertex_endpoint_env_vars_skipped_if_base_url():
    """Test env vars are not populated when base_url is provided."""
    with unittest.mock.patch.dict(
        os.environ,
        {"GOOGLE_CLOUD_PROJECT": "env-project", "GOOGLE_CLOUD_LOCATION": "env-location"}
    ):
        endpoint = models.VertexEndpoint(base_url="https://example.com")
        assert endpoint.project is None
        assert endpoint.location is None


def test_vertex_endpoint_env_vars_skipped_if_api_key():
    """Test env vars are not populated when api_key is provided."""
    with unittest.mock.patch.dict(
        os.environ,
        {"GOOGLE_CLOUD_PROJECT": "env-project", "GOOGLE_CLOUD_LOCATION": "env-location"}
    ):
        endpoint = models.VertexEndpoint(api_key="secret")
        assert endpoint.project is None
        assert endpoint.location is None


def test_vertex_endpoint_validate_base_url():
    """Test validation succeeds when base_url is set."""
    endpoint = models.VertexEndpoint(base_url="https://example.com")
    endpoint.validate_endpoint()  # Should not raise


def test_vertex_endpoint_validate_standard_auth():
    """Test validation succeeds when project and location are provided."""
    # Prevent env vars from populating missing fields
    env_copy = os.environ.copy()
    env_copy.pop("GOOGLE_CLOUD_PROJECT", None)
    env_copy.pop("GOOGLE_CLOUD_LOCATION", None)
    with unittest.mock.patch.dict(os.environ, env_copy, clear=True):
        endpoint = models.VertexEndpoint(project="test-project", location="us-central1")
        endpoint.validate_endpoint()  # Should not raise


def test_vertex_endpoint_validate_express_auth():
    """Test validation succeeds when api_key is provided."""
    env_copy = os.environ.copy()
    env_copy.pop("GOOGLE_CLOUD_PROJECT", None)
    env_copy.pop("GOOGLE_CLOUD_LOCATION", None)
    with unittest.mock.patch.dict(os.environ, env_copy, clear=True):
        endpoint = models.VertexEndpoint(api_key="secret")
        endpoint.validate_endpoint()  # Should not raise


def test_vertex_endpoint_validate_mixed_auth():
    """Test validation fails when mixing standard and express auth."""
    # mixing standard (project/location) and express (api_key)
    with pytest.raises(ValueError, match="Cannot specify both api_key"):
        endpoint = models.VertexEndpoint(project="test-project", api_key="secret")
        endpoint.validate_endpoint()

    with pytest.raises(ValueError, match="Cannot specify both api_key"):
        endpoint = models.VertexEndpoint(location="us-central1", api_key="secret")
        endpoint.validate_endpoint()


def test_vertex_endpoint_validate_incomplete_auth():
    """Test validation fails when authentication is incomplete."""
    env_copy = os.environ.copy()
    env_copy.pop("GOOGLE_CLOUD_PROJECT", None)
    env_copy.pop("GOOGLE_CLOUD_LOCATION", None)
    with unittest.mock.patch.dict(os.environ, env_copy, clear=True):
        endpoint = models.VertexEndpoint(project="test-project")
        with pytest.raises(ValueError, match="either \\(project and location\\) or api_key must be set"):
            endpoint.validate_endpoint()

        endpoint = models.VertexEndpoint(location="us-central1")
        with pytest.raises(ValueError, match="either \\(project and location\\) or api_key must be set"):
            endpoint.validate_endpoint()

        endpoint = models.VertexEndpoint()
        with pytest.raises(ValueError, match="either \\(project and location\\) or api_key must be set"):
            endpoint.validate_endpoint()


def test_model_target_defaults():
    """Test default values for ModelTarget."""
    target = models.ModelTarget(name="test-model")
    assert target.types == [models.ModelType.TEXT]


def test_model_target_types_override():
    """Test overriding default values for ModelTarget."""
    target = models.ModelTarget(name="test-model", types=[models.ModelType.IMAGE])
    assert target.types == [models.ModelType.IMAGE]
