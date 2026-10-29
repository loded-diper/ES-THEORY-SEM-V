"""Checks the pipeline's failure modes and separation, not claimed real-world accuracy."""
import unittest
import numpy as np
import torch
from demo import (make_data, preprocess, window, decide, classification_metrics,
                  GestureGRU, generate_recording, SEED)


class PipelineTests(unittest.TestCase):
    def test_split_groups_and_dimensions(self):
        data, _, _, manifest = make_data()
        groups = [set(v[2]) for v in data.values()]
        self.assertFalse(groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2])
        self.assertEqual(len({r['generator_seed'] for r in manifest}), len(manifest))
        self.assertEqual(tuple(data['test'][0].shape), (200,64,6))

    def test_normalization_training_only(self):
        _, mean, std, manifest = make_data()
        x = np.concatenate([preprocess(generate_recording(
            ['background','swipe_left','swipe_right','wave'].index(r['label']),
            r['generator_seed'])) for r in manifest if r['split']=='train'])
        np.testing.assert_allclose(mean, x.mean(0), atol=1e-6)
        np.testing.assert_allclose(std, x.std(0), atol=1e-6)

    def test_causal_filter(self):
        a = generate_recording(1, SEED)
        b = a.copy(); b[100:] += 10
        np.testing.assert_array_equal(preprocess(a)[:100], preprocess(b)[:100])

    def test_invalid_input(self):
        for x in [np.zeros((64,3)), np.zeros((10,6)), np.full((64,6),np.nan)]:
            with self.assertRaises(ValueError): preprocess(x)

    def test_command_rejection(self):
        self.assertEqual(decide(np.ones(4)/4)[2], 'NO_COMMAND')
        self.assertEqual(decide(np.array([.85,.05,.05,.05]))[2], 'NO_COMMAND')
        self.assertEqual(decide(np.array([.01,.01,.97,.01]))[2], 'LIGHT_ON')
        self.assertEqual(decide(np.array([.1,.1,.7,.1]))[2], 'NO_COMMAND')

    def test_metrics_against_known_confusion(self):
        r = classification_metrics(np.array([0,1,2,3]), np.array([0,1,1,3]))
        self.assertAlmostEqual(r['accuracy'], .75)
        self.assertAlmostEqual(r['macro_f1'], 2/3)

    def test_model_and_window_shape(self):
        x = window(preprocess(generate_recording(3, SEED)))
        self.assertEqual(x.shape, (5,64,6))
        self.assertEqual(tuple(GestureGRU()(torch.tensor(x)).shape), (5,4))


if __name__ == '__main__':
    unittest.main()
