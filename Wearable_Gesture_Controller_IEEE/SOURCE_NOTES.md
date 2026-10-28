# Source provenance and analytical checks

## Primary project source

The supplied `ICT_3132_ES_Synopsis_Wearable_Gesture_Controller.docx` provides the title, accessibility motivation, six-axis IMU concept, local inference, optional BLE/Wi-Fi path, LSTM baseline, lightweight-model direction, compression ideas, and example boards. The user's later request explicitly changes the scope to a theoretical report and corrects Vishad Sharma's registration number to 240911680. The source document's plans are treated as proposed work, not evidence of an implementation.

## IEEE template components

`IEEEtran.cls` (2015/08/26, V1.8b) and `IEEEtran.bst` (2015/08/26, V1.14) are unmodified upstream IEEEtran components obtained from Debian's TeX Live publishers package over HTTPS:

https://deb.debian.org/debian/pool/main/t/texlive-extra/texlive-publishers_2024.20250309-2_all.deb

The upstream project is identified in the class header:

- https://www.ctan.org/pkg/ieeetran
- https://www.michaelshell.org/tex/ieeetran/

Copyright, license, and redistribution notices are retained inside both files. The report uses the class's conference option and IEEEtran's bibliography style without modifying the supplied class or style. `main.tex` contains the report-specific content.

## Research references

1. S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” *Neural Computation*, 9(8), 1735–1780, 1997. DOI: https://doi.org/10.1162/neco.1997.9.8.1735. The Keras LSTM source also identifies its Hochreiter 1997 basis: https://github.com/keras-team/keras/blob/master/keras/src/layers/rnn/lstm.py.
2. K. Cho et al., “Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation,” EMNLP 2014, 1724–1734. DOI: https://doi.org/10.3115/v1/D14-1179. Exact title, authors, pages, and DOI were checked against ACL Anthology's own XML record (`paper id="179"`): https://github.com/acl-org/acl-anthology/blob/master/data/xml/D14.xml.
3. F. J. Ordóñez and D. Roggen, “Deep Convolutional and LSTM Recurrent Neural Networks for Multimodal Wearable Activity Recognition,” *Sensors*, 16(1), article 115, 2016. DOI: https://doi.org/10.3390/s16010115. The authors' implementation repository identifies and links the paper: https://github.com/STRCWearlab/DeepConvLSTM.
4. B. Jacob et al., “Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference,” CVPR 2018, 2704–2713. DOI: https://doi.org/10.1109/CVPR.2018.00286. TensorFlow Model Optimization's own documentation identifies and links the paper (arXiv:1712.05877): https://github.com/tensorflow/model-optimization/blob/master/tensorflow_model_optimization/g3doc/guide/quantization/training.md. The supporting affine quantization explanation is also available in Google's gemmlowp documentation: https://github.com/google/gemmlowp/blob/master/doc/quantization.md. The report does not claim this paper establishes integer-GRU runtime support.
5. C. Banbury et al., “MLPerf Tiny Benchmark,” *Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks*, vol. 1, 2021. Stable preprint: https://arxiv.org/abs/2106.07597. Title, citation, and scope were checked against MLCommons' own repository: https://github.com/mlcommons/tiny.

The report cites these papers for their relevant concepts, not as evidence of the proposed controller's performance. Publisher/Crossref endpoints were unavailable under the current network policy; accessible author/organization repositories supplied the cross-checks noted above. No additional unverified papers or benchmark claims were introduced.

## Analytical calculations

Illustrative assumptions: six inputs, five output classes, one recurrent layer, final hidden-state classification, a dense output head, one bias per gate, and 64 samples per window.

- LSTM with h=32: `4*32*(6+32+1) + (32+1)*5 = 5157` parameters.
- GRU with h=24: `3*24*(6+24+1) + (24+1)*5 = 2357` parameters.
- A reset-after GRU with a second bias vector per gate adds `3*24 = 72` parameters; the report explicitly distinguishes that variant.
- FP32 parameter payloads: `5157*4/1024 = 20.1445 KiB` and `2357*4/1024 = 9.2070 KiB`.
- Parameter reduction: `(1 - 2357/5157)*100 = 54.2951%`.
- Matrix MACs including a final dense head: LSTM `64*4*32*(6+32) + 32*5 = 311456`; GRU `64*3*24*(6+24) + 24*5 = 138360`.
- The MAC counts exclude gating products, nonlinearities, preprocessing, and runtime overhead.
- Window duration: `64/50 = 1.28 s`; stride interval: `16/50 = 0.32 s`. These are not measured response delays.
- Input buffer alone: `64*6*2 = 768 bytes` for 16-bit samples, or `64*6*4 = 1536 bytes` for FP32.

These are calculations from a specification, not experimental outcomes. Training quality, converted-artifact size, MCU performance, and energy remain unknown.
