import unittest
from google.antigravity.connections.local import local_connection_config
from google.antigravity import types
from google.antigravity.models import DEFAULT_MODEL, DEFAULT_IMAGE_GENERATION_MODEL

class LocalConnectionConfigTest(unittest.TestCase):

    def test_merge_models_list_empty(self):
        config = local_connection_config.LocalAgentConfig()
        models = config.models
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].name, DEFAULT_MODEL)
        self.assertEqual(models[0].types, [types.ModelType.TEXT])
        self.assertEqual(models[1].name, DEFAULT_IMAGE_GENERATION_MODEL)
        self.assertEqual(models[1].types, [types.ModelType.IMAGE])

    def test_merge_models_list_shorthand_string(self):
        config = local_connection_config.LocalAgentConfig(model="my-custom-model")
        models = config.models
        self.assertEqual(len(models), 2)
        # Priority: Shorthand > Default
        self.assertEqual(models[0].name, "my-custom-model")
        self.assertEqual(models[0].types, [types.ModelType.TEXT])

        self.assertEqual(models[1].name, DEFAULT_IMAGE_GENERATION_MODEL)
        self.assertEqual(models[1].types, [types.ModelType.IMAGE])

    def test_merge_models_list_shorthand_model_target_image(self):
        image_model = types.ModelTarget(name="my-image-model", types=[types.ModelType.IMAGE])
        config = local_connection_config.LocalAgentConfig(model=image_model)
        models = config.models
        self.assertEqual(len(models), 2)

        self.assertEqual(models[0].name, "my-image-model")
        self.assertEqual(models[0].types, [types.ModelType.IMAGE])

        self.assertEqual(models[1].name, DEFAULT_MODEL)
        self.assertEqual(models[1].types, [types.ModelType.TEXT])

    def test_merge_models_list_explicit_models_text(self):
        explicit_text_model = types.ModelTarget(name="explicit-text-model", types=[types.ModelType.TEXT])
        config = local_connection_config.LocalAgentConfig(models=[explicit_text_model])
        models = config.models

        self.assertEqual(len(models), 2)

        self.assertEqual(models[0].name, "explicit-text-model")
        self.assertEqual(models[0].types, [types.ModelType.TEXT])

        self.assertEqual(models[1].name, DEFAULT_IMAGE_GENERATION_MODEL)
        self.assertEqual(models[1].types, [types.ModelType.IMAGE])

    def test_merge_models_list_explicit_models_both(self):
        explicit_text = types.ModelTarget(name="explicit-text", types=[types.ModelType.TEXT])
        explicit_image = types.ModelTarget(name="explicit-image", types=[types.ModelType.IMAGE])
        config = local_connection_config.LocalAgentConfig(models=[explicit_text, explicit_image])
        models = config.models

        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].name, "explicit-text")
        self.assertEqual(models[1].name, "explicit-image")

    def test_merge_models_list_explicit_and_shorthand(self):
        explicit_text = types.ModelTarget(name="explicit-text", types=[types.ModelType.TEXT])
        config = local_connection_config.LocalAgentConfig(
            models=[explicit_text],
            model=types.ModelTarget(name="shorthand-image", types=[types.ModelType.IMAGE])
        )
        models = config.models

        # Priority: Explicit > Shorthand > Default
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].name, "explicit-text")
        self.assertEqual(models[1].name, "shorthand-image")

        # What if both are text? Then image should be appended from default
        config_both_text = local_connection_config.LocalAgentConfig(
            models=[explicit_text],
            model="shorthand-text"
        )
        models_both_text = config_both_text.models
        self.assertEqual(len(models_both_text), 3)
        self.assertEqual(models_both_text[0].name, "explicit-text")
        self.assertEqual(models_both_text[1].name, "shorthand-text")
        self.assertEqual(models_both_text[2].name, DEFAULT_IMAGE_GENERATION_MODEL)


if __name__ == "__main__":
    unittest.main()
