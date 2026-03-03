# Introduction {#sec:intro}

Stable, controllable, and human-like speech synthesis is widely viewed
as a key capability on the path to AGI. Modern neural text-to-speech
(TTS) models, trained on large-scale datasets, already deliver
exceptional capability to generate high-quality speech from a few
seconds of reference
audio [@valle; @naturalspeech2; @naturalspeech3; @uniaudio; @e2tts; @f5tts; @cosyvoice; @sparktts; @maskgct; @llasa].
Among them, discrete speech tokenization [@Encodec; @SoundStream; @dac]
combined with autoregressive language modeling of discrete units has
gained traction, offering improved stability while preserving high
naturalness and
human-likeness [@cosyvoice3; @fish-speech-v1.4; @moshi; @qwen2.5omni; @minimax-speech].
Conditioning on vocal features or text instructions facilitates
finer-grained control over prosody and style, resulting in outputs of
greater richness and
diversity [@cosyvoice2; @parlertts; @voxinstruct; @controlspeech; @prompttts2].
These breakthroughs are paving the way for diverse applications in
fields such as virtual assistants and automated content creation.

In this report, we take a step toward stable, controllable, and
human-like speech synthesis and introduce Qwen3-TTS, the first
text-to-speech model in the Qwen series. Qwen3-TTS exhibits the
following properties: 1) **Controllability**: Qwen3-TTS allows users to
create new voices or manipulate fine-grained attributes of generated
speech via natural language descriptions, while also supporting the
stable generation of any content using the created voice. 2) **Voice
Cloning and Predefined Voice Profiles**: Qwen3-TTS supports 3-second
voice cloning and generation using a set of x curated, high-quality
preset voices. 3) **Naturalness**: Beyond achieving robust synthesis,
Qwen3-TTS excels in generating highly natural and expressive speech. Our
1.7B model, in particular, delivers state-of-the-art, human-like
quality, demonstrating our approach successfully maximizes perceptual
quality without overfitting to ASR-related metrics.
4) **Multilinguality**: The model is trained across more than 10
languages and supports speaker-consistent multilingual generation.
5) **Streaming**: Designed for streaming text input and streaming audio
output, it achieves a first-packet latency as low as 97 ms (0.6B
variant) and 101 ms (1.7B variant).

Beyond the aforementioned aspects, and from a broader perspective of
practical application, it is crucial for our model to integrate
seamlessly with Large Language Models (LLMs) and achieve extremely low
first-packet latency. To this end, we use discrete speech
representations as the cornerstone of our architecture and introduce two
tokenizers in the Qwen3-TTS family: 1) *Qwen-TTS-Tokenizer-25Hz* employs
a 25 Hz single-codebook representation with waveform reconstruction via
block-wise flow matching to enable streaming synthesis [@qwen2.5omni].
Empirically, we find that semantic tokenizers lack expressive power,
whereas purely acoustic tokenizers inject excessive low-level detail
that complicates LLM-based modeling and leads to long-horizon error
accumulation. To balance these factors, Qwen-TTS-Tokenizer-25Hz
integrates semantic and acoustic cues, leveraging the Qwen2-Audio
encoder for both expressivity and tractability. Although it supports
streaming with a block-wise diffusion decoder, we found that its
single-codebook design limits suitability for ultra-low-latency
applications and general speech synthesis. Therefore, we develop 2)
*Qwen-TTS-Tokenizer-12Hz*, which adopts a 12.5 Hz multi-codebook scheme
inspired by @zhang2023speechtokenizer. Its first codebook layer encodes
semantic content, while the subsequent layers capture acoustic details.
The increased capacity permits waveform reconstruction using only a
lightweight causal ConvNet, eliminating the need for speaker vector
extraction or complex diffusion models [@cosyvoice2; @minimax-speech].
To further support ultra--low-latency streaming, we designed a
dual-track autoregressive architecture for streaming text input and
audio output. This architecture incorporates a Multi-Token Prediction
(MTP) module to effectively model the multi-codebook sequence, which
enables immediate speech decoding from the first codec frame.

Trained on over 5 million hours of speech data, Qwen3-TTS achieves
impressive performance across diverse benchmarks. Specifically, it
establishes a new state-of-the-art in zero-shot voice cloning, achieving
the lowest Word Error Rate (WER) on the Seed-TTS benchmark while
delivering superior speaker similarity across all 10 evaluated languages
compared to commercial baselines like MiniMax and ElevenLabs. In
cross-lingual scenarios, Qwen3-TTS demonstrates exceptional
adaptability, reducing error rates by significant margins in challenging
pairs such as Chinese-to-Korean. Regarding controllability, Qwen3-TTS
excels in following complex natural language instructions for voice
design and control, outperforming GPT-4o-mini-tts in target speaker
manipulation. Furthermore, the model exhibits remarkable stability in
long-form generation, capable of synthesizing over 10 minutes of natural
and fluent speech. To facilitate community research and development, we
release the complete family of Qwen3-TTS models and tokenizers.

# Qwen-TTS-Tokenizer

## Qwen-TTS-Tokenizer-25Hz

#### Tokenizer

Qwen-TTS-Tokenizer-25 Hz is a 25 Hz single-codebook tokenizer built upon
Qwen2-Audio through a two-stage training framework. In the first stage
(Stage 1), we continue pretraining Qwen2-Audio on an automatic speech
recognition (ASR) task, augmenting the audio encoder with an additional
resampling layer and a vector quantization (VQ) layer inserted at an
intermediate position. In the second stage (Stage 2), we fine-tune the
entire model by incorporating a convolution-based mel-spectrogram
decoder, which reconstructs mel-spectrograms from the audio tokens. This
reconstruction objective explicitly injects essential acoustic
information into the learned audio token representations.

#### Streaming Detokenizer

To enable streaming audio generation, particularly for long sequences,
we propose a sliding-window block attention mechanism that restricts
each token to a limited context. Specifically, we use a Diffusion
Transformer (DiT) trained with Flow Matching [@flowmatching]. The input
code sequence is first mapped to a mel-spectrogram via Flow Matching,
after which a modified BigVGAN [@sangbigvgan] reconstructs the waveform
from the generated mel-spectrogram.

To support streaming decoding, we group adjacent codes into fixed-length
blocks and construct the corresponding attention mask [@streamflow]. The
DiT's receptive field is restricted to 4 blocks---the current block, a
3-block lookback, and a 1-block lookahead. During decoding, we generate
mel-spectrograms in chunks with Flow Matching, ensuring that each code
chunk has access to the required context blocks. This design improves
streaming quality by preserving necessary context. We apply the same
chunked procedure to BigVGAN, whose receptive field is fixed, to support
streaming waveform synthesis.

## Qwen-TTS-Tokenizer-12Hz

Qwen-TTS-Tokenizer-12Hz is a 12.5 Hz multi-codebook tokenizer with
jointly optimized semantic and acoustic streams. Building on the
semantic--acoustic disentangled quantization strategy of the Mimi
architecture [@moshi], speech is decomposed into two discrete code
sequences: a semantic codebook capturing high-level semantic content and
an acoustic codebook modeling acoustic detail, prosody, and others.
Training adopts a GAN-based framework in which the generator operates
directly on raw waveforms to extract and quantize both representations,
while the discriminator improves the naturalness and fidelity of
reconstructed speech. A multi-scale mel-spectrogram reconstruction loss
further enforces time--frequency consistency. For the semantic path,
WavLM [@wavlm] serves as a teacher to guide the first semantic codebook
layer toward semantically aligned features. The acoustic path employs a
15-layer residual vector quantization (RVQ) module that progressively
refines details not captured by the semantic codebook. To enable
streaming, we use fully causal feature encoders and decoders: the
encoder processes frames sequentially and emits semantic and acoustic
tokens at 12.5 Hz without look-ahead, and the decoder reconstructs audio
incrementally from these tokens. This end-to-end causal design supports
streaming inference with low latency, making the tokenizer suitable for
real-time online services.

# Method

## Architectures

Qwen3-TTS leverages the Qwen3 LM family to achieve high concurrency and
low-latency inference. Text is processed using the standard Qwen
tokenizer, while speech is encoded using the Qwen-TTS-Tokenizer. To
maintain precise identity control, we jointly train a learnable speaker
encoder with the backbone. For real-time synthesis, Qwen3-TTS employs a
dual-track representation by concatenating textual and acoustic tokens
along the channel axis. Upon receiving a textual token, the model
immediately predicts the corresponding acoustic tokens, which are then
converted into waveforms by the Code2Wav module.

#### Qwen3-TTS-25Hz

Qwen3-TTS-25Hz uses Qwen-TTS-Tokenizer-25Hz to extract single-level
speech tokens. The backbone integrates text features with preceding
speech tokens and predicts the current speech token through a linear
head. The resulting sequence is then processed by a chunk-wise DiT
module for high-fidelity waveform reconstruction.

#### Qwen3-TTS-12Hz

Architecturally, Qwen3-TTS-12Hz differs from Qwen3-TTS-25Hz by operating
on RVQ tokens from Qwen-TTS-Tokenizer-12Hz. It adopts a hierarchical
prediction scheme: the backbone ingests aggregated codebook features to
predict the zeroth codebook, and an MTP (Multi-Token Prediction) module
then generates all residual codebooks. This strategy captures intricate
acoustic details, significantly enhancing vocal consistency and
expressivity, while minimizing latency through single-frame instant
generation.

## Training

The training process consists of pre-training and post-training. All
data is formatted in ChatML to standardize inputs and support
controllable speech generation.

The pre-training of Qwen3-TTS is structured into three stages:

1.  **General Stage (S1)**: During the initial pre-training phase, we
    leverage over 5 million hours of multilingual speech data to train
    Qwen3-TTS. This stage establishes a monotonic mapping from
    multilingual text representations to speech and builds general
    capabilities for Qwen3-TTS.

2.  **High-Quality Stage (S2)**: We stratify data quality with a
    dedicated pipeline and perform continual pre-training (CPT) with
    high-quality data. This stage alleviates hallucinations caused by
    noisy data in the initial stage and significantly improves the
    quality of generated speech.

3.  **Long-Context Stage (S3)**: In the final pre-training phase, we
    increase the maximum token length from 8,192 to 32,768 and upsample
    long speech in the training data. Experimental results indicate that
    these adjustments enhance the model's ability to process extended
    and complex inputs and to generate contextually appropriate speech
    responses.

The post-training phase comprises three stages, enabling Qwen3-TTS to
generate human-like speech and remain stable across tasks. In the first
stage, we introduce Direct Preference Optimization
(DPO) [@rafailov2024direct] to align model outputs with human
preferences. Specifically, we construct preference pairs for
multilingual speech samples based on human feedback and then perform DPO
on Qwen3-TTS. In the second stage, we employ rule-based rewards and
leverage GSPO to comprehensively enhance the model's capabilities and
stability across tasks. Finally, we introduce lightweight speaker
fine-tuning on the base model, enabling Qwen3-TTS to adopt specific
voices while further improving the naturalness, expressiveness, and
controllability of its speech responses.

## Features

Qwen3-TTS supports streaming voice cloning, voice design, and
fine-grained control. To achieve this, we prepend user-provided
instructions containing fine-grained control signals to the input
sequences.

For voice cloning, Qwen3-TTS clones a target voice from (i) reference
speech via a speaker embedding, enabling real-time cloning, or (ii) a
text--speech pair via in-context learning, which better preserves
prosody. For voice design, built upon the Qwen3 text model foundation,
Qwen3-TTS inherits robust text comprehension capabilities. Additionally,
we introduce a probabilistically activated *thinking pattern* during
training to improve instruction following, especially for complex
descriptions. Furthermore, based on this strong instruction-following
capability, Qwen3-TTS controls predefined voices with desired styles.

## Efficiency

Low first-packet latency and stable streaming under concurrency are
jointly determined by (i) the language model (LM) time to first token
group for the first speech packet, and (ii) the tokenizer decoding
pipeline that converts generated tokens into waveforms. As shown in
Table [1](#tab:qwen3tts_efficiency){reference-type="ref"
reference="tab:qwen3tts_efficiency"}, we evaluate Qwen3-TTS with
different LM sizes and tokenizer variants under various concurrency
levels. All reported numbers are end-to-end measured latencies, and
steady-state costs are measured per speech packet during streaming
generation. Specifically, latency is measured on our internal vLLM
engine (vLLM V0 backend) on a single typical computational resource with
optimizations applied via *torch.compile* and CUDA Graph acceleration to
the decoding stage of the tokenizer. Reported First-Packet Latency is
the sum of LM time-to-first packet tokens (TTFP) and tokenizer decode
time for per-packet (TPP). LM time for per-packet (TPP) is the
steady-state LM time to produce one packet's tokens during streaming
generation.

[]{#tab:qwen3tts_efficiency label="tab:qwen3tts_efficiency"}

Qwen-TTS-Tokenizer-25Hz performs code-to-waveform synthesis through
chunk-wise inference. Due to the look-ahead requirement in the DiT
module, waveform synthesis for the first chunk cannot start until
sufficient future tokens are available. With a chunk size of 8 set in
Qwen3-TTS, the model must wait for the LM to generate 16 tokens before
DiT can produce the first 8-token mel chunk. Under the 25 Hz token rate
(40 ms per token), this corresponds to 320 ms of mel content per packet.
In addition, the BigVGAN vocoder introduces an extra right-context
look-ahead (130 ms). Therefore, for Tokenizer-25Hz, the first packet
ultimately contains about 190 ms of audio, and the LM must generate 16
tokens before synthesis can start. During steady-state streaming
generation, every time the LM generates 8 tokens, DiT and BigVGAN can
synthesize a 320 ms audio packet. The first-packet latency and RTF
reported in our table are computed based on the above setup.

Qwen-TTS-Tokenizer-12Hz uses a pure left-context streaming codec
decoder, enabling waveform emission immediately after the required
tokens are available, without waiting for future context. With the 12.5
Hz token rate, each token corresponds to 80 ms of audio, so one token
can be decoded into audio directly in principle. To avoid excessive
scheduling overhead caused by very small packets, we define one speech
packet as 4 tokens, which means 320 ms of speech per packet. This design
significantly reduces decoding time and yields lower first-packet
latency, while maintaining low RTF under higher concurrency due to the
lightweight and batch-friendly codec decoder.
