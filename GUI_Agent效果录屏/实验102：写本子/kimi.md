# Introduction

Large Language Models (LLMs) are rapidly evolving toward agentic
intelligence. Recent advances, such as GPT-5.2 [@gpt52report], Claude
Opus 4.5 [@opus45report], Gemini 3 Pro [@gemini3pro], and Kimi
K2-Thinking [@moonshotai2025kimi], demonstrate substantial progress in
agentic capabilities, particularly in tool calling and reasoning. These
models increasingly exhibit the ability to decompose complex problems
into multi-step plans and to execute long sequences of interleaved
reasoning and actions.

In this report, we introduce the training methods and evaluation results
of Kimi K2.5. Concretely, we improve the training of K2.5 over previous
models in the following two key aspects.

**Joint Optimization of Text and Vision.** A key insight from the
practice of K2.5 is that joint optimization of text and vision enhances
both modalities and avoids the conflict. Specifically, we devise a set
of techniques for this purpose. During pre-training, in contrast to
conventional approaches that add visual tokens to a text backbone at a
late
stage [@bai2025qwen3vltechnicalreport; @guo2025seed15vltechnicalreport],
we find early vision fusion with lower ratios tends to yield better
results given the fixed total vision-text tokens. Therefore, K2.5 mixes
text and vision tokens with a constant ratio throughout the entire
training process.

Architecturally, Kimi K2.5 employs MoonViT-3D, a native-resolution
vision encoder incorporating the NaViT packing
strategy [@dehghani2023patchnpacknavit], enabling variable-resolution
image inputs. For video understanding, we introduce a lightweight 3D ViT
compression mechanism: consecutive frames are grouped in fours,
processed through the shared MoonViT encoder, and temporally averaged at
the patch level. This design allows Kimi K2.5 to process videos up to 4
$\times$ longer within the same context window while maintaining
complete weight sharing between image and video encoders.

During post-training, we introduce zero-vision SFT---text-only SFT alone
activates visual reasoning and tool use. We find that adding
human-designed visual trajectories at this stage hurts generalization.
In contrast, text-only SFT performs better---likely because joint
pretraining already establishes strong vision-text alignment, enabling
capabilities to generalize naturally across modalities. We then apply
joint RL on both text and vision tasks. Crucially, we find visual RL
enhances textual performance rather than degrading it, with improvements
on MMLU-Pro and GPQA-Diamond. This bidirectional enhancement---text
bootstraps vision, vision refines text---represents superior cross-modal
alignment in joint training.

**Agent Swarm: Parallel Agent Orchestration.** Most existing agentic
models rely on sequential execution of tool calls. Even systems capable
of hundreds of reasoning steps, such as Kimi
K2-Thinking [@moonshotai2025kimi], suffer from linear scaling of
inference time, leading to unacceptable latency and limiting task
complexity. As agentic workloads grow in scope and heterogeneity---e.g.,
building a complex project that involves massive-scale research, design,
and development---the sequential paradigm becomes increasingly
inefficient.

To overcome the latency and scalability limits of sequential agent
execution, Kimi K2.5 introduces *Agent Swarm*, a dynamic framework for
parallel agent orchestration. We propose a Parallel-Agent Reinforcement
Learning (PARL) paradigm that departs from traditional agentic
RL [@moonshotai2025kimiresearcher]. In addition to optimizing tool
execution via verifiable rewards, the model is equipped with interfaces
for sub-agent creation and task delegation. During training, sub-agents
are frozen and their execution trajectories are excluded from the
optimization objective; only the orchestrator is updated via
reinforcement learning. This decoupling circumvents two challenges of
end-to-end co-optimization: credit assignment ambiguity and training
instability. Agent Swarm enables complex tasks to be decomposed into
heterogeneous sub-problems executed concurrently by domain-specialized
agents, transforming task complexity from linear scaling to parallel
processing. In wide-search scenarios, Agent Swarm reduces inference
latency by up to 4.5$\times$ while improving item-level F1 from 72.8% to
79.0% compared to single-agent baselines.

Kimi K2.5 represents a unified architecture for general-purpose agentic
intelligence, integrating vision and language, thinking and instant
modes, chats and agents. It achieves strong performance across a broad
range of agentic and frontier benchmarks, including state-of-the-art
results in visual-to-code generation (image/video-to-code) and
real-world software engineering in our internal evaluations, while
scaling both the diversity of specialized agents and the degree of
parallelism. To accelerate community progress toward General Agentic
Intelligence, we open-source our post-trained checkpoints of Kimi K2.5,
enabling researchers and developers to explore, refine, and deploy
scalable agentic intelligence.

# Joint Optimization of Text and Vision

Kimi K2.5 is a native multimodal model built upon Kimi K2 through
large-scale joint pre-training on approximately 15 trillion mixed visual
and text tokens. Unlike vision-adapted models that compromise either
linguistic or visual capabilities, our joint pre-training paradigm
enhances both modalities simultaneously. This section describes the
multimodal joint optimization methodology that extends Kimi K2 to Kimi
K2.5.

## Native Multimodal Pre-Training {#sec:joint-pre}

A key design question for multimodal pre-training is: Given a fixed
vision-text token budget, what is the optimal vision-text joint-training
strategy. Conventional
wisdom [@bai2025qwen3vltechnicalreport; @guo2025seed15vltechnicalreport]
suggests introducing vision tokens predominantly in the later stages of
LLM training at high ratios (e.g., 50% or higher) should accelerate
multimodal capability acquisition, treating multimodal capability as a
post-hoc add-on to linguistic competence.

However, our experiments (as shown in
Table [1](#tab:joint-train){reference-type="ref"
reference="tab:joint-train"}
Figure [\[fig:joint-train\]](#fig:joint-train){reference-type="ref"
reference="fig:joint-train"}) reveal a different story. We conducted
ablation studies varying the vision ratio and vision injection timing
while keeping the total vision and text token budgets fixed. To strictly
meet the targets for different ratios, we pre-trained the model with
text-only tokens for a specifically calculated number of tokens before
introducing vision data. Surprisingly, we found that the vision ratio
has minimal impact on final multimodal performance. In fact, **early
fusion with a lower vision ratio yields better results given a fixed
total vision-text token budget**. This motivates our native multimodal
pre-training strategy: rather than aggressive vision-heavy training
concentrated at the end, we adopt a moderate vision ratio integrated
early in the training process, allowing the model to naturally develop
balanced multimodal representations while benefiting from extended
co-optimization of both modalities.

## Zero-Vision SFT

Pretrained VLMs do not naturally perform vision-based tool-calling,
which poses a cold-start problem for multimodal RL. Conventional
approaches address this issue through manually annotated or
prompt-engineered chain-of-thought (CoT)
data [@bai2025qwen3vltechnicalreport], but such methods are limited in
diversity, often restricting visual reasoning to simple diagrams and
primitive tool manipulations (`crop`, `rotate`, `flip`).

An observation is that high-quality text SFT data are relatively
abundant and diverse. We propose a novel approach, zero-vision SFT, that
uses only text SFT data to activate the visual, agentic capabilities
during post-training. In this approach, all image manipulations are
proxied through programmatic operations in `IPython`, effectively
serving as a generalization of traditional vision tool-use. This
\"zero-vision\" activation enables diverse reasoning behaviors,
including pixel-level operations such as object size estimation via
binarization and counting, and generalizes to visually grounded tasks
such as object localization, counting, and OCR.

Figure [1](#fig:visionzerorl_curves){reference-type="ref"
reference="fig:visionzerorl_curves"} illustrates the RL training curves,
where the starting points are obtained from zero-vision SFT. The results
show that zero-vision SFT is sufficient for activating vision
capabilities while ensuring generalization across modalities. This
phenomenon is likely due to the joint pretraining of text and vision
data as described in Section [2.1](#sec:joint-pre){reference-type="ref"
reference="sec:joint-pre"}. Compared to zero-vision SFT, our preliminary
experiments show that text-vision SFT yields much worse performance on
visual, agentic tasks, possibly because of the lack of high-quality
vision data.

## Joint Multimodal Reinforcement Learning (RL) {#sec:native_multimodal_rl}

In this section, we describe the methodology implemented in K2.5 that
enables effective multimodal RL, from outcome-based visual RL to
emergent cross-modal transfer that enhances textual performance.

#### Outcome-Based Visual RL

Following the zero-vision SFT, the model requires further refinement to
reliably incorporate visual inputs into reasoning. Text-initiated
activation alone exhibits notable failure modes: visual inputs are
sometimes ignored, and images may not be attended to when necessary. We
employ outcome-based RL on tasks that explicitly require visual
comprehension for correct solutions. We categorize these tasks into
three domains:

- **Visual grounding and counting:** Accurate localization and
  enumeration of objects within images;

- **Chart and document understanding:** Interpretation of structured
  visual information and text extraction;

- **Vision-critical STEM problems:** Mathematical and scientific
  questions filtered to require visual inputs.

Outcome-based RL on these tasks improves both basic visual capabilities
and more complex agentic behaviors. Extracting these trajectories for
rejection-sampling fine-tuning (RFT) enables a self-improving data
pipeline, allowing subsequent joint RL stages to leverage richer
multimodal reasoning traces.

#### Visual RL Improves Text Performance

To investigate potential trade-offs between visual and textual
performance, we evaluated text-only benchmarks before and after visual
RL. Surprisingly, outcome-based visual RL produced measurable
improvements in textual tasks, including MMLU-Pro (84.7% $\rightarrow$
86.4%), GPQA-Diamond (84.3% $\rightarrow$ 86.4%), and LongBench v2
(56.7% $\rightarrow$ 58.9%)
(Table [2](#tab:vision_rl_text){reference-type="ref"
reference="tab:vision_rl_text"}). Analysis suggests that visual RL
enhances calibration in areas requiring structured information
extraction, reducing uncertainty on queries that resemble visually
grounded reasoning (e.g., counting, OCR). These findings indicate that
visual RL can contribute to cross-modal generalization, improving
textual reasoning without observable degradation of language
capabilities.

**Joint Multimodal RL** Motivated by the finding that robust visual
capabilities can emerge from zero-vision SFT paired with vision
RL---which further enhances general text abilities---we adopt a joint
multimodal RL paradigm during Kimi K2.5's post-training. Departing from
conventional modality-specific expert divisions, we organize RL domains
not by input modality but by abilities---knowledge, reasoning, coding,
agentic, etc. These domain experts jointly learn from both pure-text and
multimodal queries, while the Generative Reward Model (GRM) similarly
optimizes across heterogeneous traces without modality barriers. This
pardaigm ensures that capability improvements acquired through either
textual or visual inputs inherently generalize to enhance related
abilities across the alternate modality, thereby maximizing cross-modal
capability transfer.

# Method Overview

## Foundation: Kimi K2 Base Model

The foundation of Kimi K2.5 is Kimi K2 [@team2025kimik2], a
trillion-parameter mixture-of-experts (MoE) transformer [@transformer]
model pre-trained on 15 trillion high-quality text tokens. Kimi K2
employs the token-efficient MuonClip
optimizer [@jordan2024muon; @liu2025muon] with QK-Clip for training
stability. The model comprises 1.04 trillion total parameters with 32
billion activated parameters, utilizing 384 experts with 8 activated per
token (sparsity of 48). For detailed descriptions of MuonClip,
architecture design, and training infrastructure, we refer to the Kimi
K2 technical report [@team2025kimik2].

## Model Architecture

The multimodal architecture of Kimi K2.5 consists of three components: a
three-dimensional native-resolution vision encoder (MoonViT-3D), an MLP
projector, and the Kimi K2 MoE language model, following the design
principles established in Kimi-VL [@team2025kimivl].

#### MoonViT-3D: Shared Embedding Space for Images and Videos

In Kimi-VL, we employ MoonViT to natively process images at their
original resolutions, eliminating the need for complex sub-image
splitting and splicing operations. Initialized from
SigLIP-SO-400M [@zhai2023sigmoidlosslanguageimage], MoonViT incorporates
the patch packing strategy from NaViT [@dehghani2023patchnpacknavit],
where single images are divided into patches, flattened, and
sequentially concatenated into 1D sequences, thereby enabling efficient
simultaneous training on images at varying resolutions.

To maximize the transfer of image understanding capabilities to video,
we introduce **MoonViT-3D** with a unified architecture, fully shared
parameters, and a consistent embedding space. By generalizing the "patch
n' pack" philosophy to the temporal dimension, up to four consecutive
frames are treated as a spatiotemporal volume: 2D patches from these
frames are jointly flattened and packed into a single 1D sequence,
allowing the identical attention mechanism to operate seamlessly across
both space and time. While the extra temporal attention improves
understanding on high-speed motions and visual effects, the sharing
maximizes knowledge generalization from static images to dynamic videos,
achieving strong video understanding performance (see in
Tab. [\[tab:instruct_eval\]](#tab:instruct_eval){reference-type="ref"
reference="tab:instruct_eval"}) without requiring specialized video
modules or architectural bifurcation. Prior to the MLP projector,
lightweight temporal pooling aggregates patches within each temporal
chunk, yielding $4\times$ temporal compression to significantly extend
feasible video length. The result is a unified pipeline where knowledge
and ability obtained from image pretraining transfers holistically to
videos through one shared parameter space and feature representation.

## Pre-training Pipeline

As illustrated in
Table [3](#tab:pretrainingdatavolume){reference-type="ref"
reference="tab:pretrainingdatavolume"}, Kimi K2.5's pre-training builds
upon the Kimi K2 language model checkpoint and processes approximately
15T tokens across three stages: first, standalone ViT training to
establish a robust native-resolution visual encoder; second, joint
pre-training to simultaneously enhance language and multimodal
capabilities; and third, mid-training on high-quality data and
long-context activation to refine capabilities and extend context
windows.

#### ViT Training Stage

The MoonViT-3D is continual pre-trained from
SigLIP [@zhai2023sigmoidlosslanguageimage] on image-text and video-text
pairs, where the text components consist of a variety of targets: image
alt texts, synthetic captions of images and videos, grounding bboxes,
and OCR texts. Unlike the implementation in Kimi-VL [@team2025kimivl],
this continual pre-training does not include a contrastive loss, but
incorporates solely cross-entropy loss ${L}_{caption}$ for caption
generation conditioned on input images and videos. We adopt a two-stage
alignment strategy. In the first stage, we update the MoonViT-3D to
align it with Moonlight-16B-A3B [@liu2025muon] via the caption loss,
consuming about 1T tokens with very few training FLOPs. This stage
allows MoonViT-3D to primarily understand high-resolution images and
videos. A very short second stage follows, updating only the MLP
projector to bridge the ViT with the 1T LLM for smoother joint
pre-training.

#### Joint Training Stages

The joint pre-training stage continues from a near-end Kimi K2
checkpoint over additional 15T vision-text tokens at 4K sequence length.
The data recipe extends Kimi K2's pre-training distribution by
introducing unique tokens, adjusting data proportions with increased
weight on coding-related content, and controlling maximum epochs per
data source. The third stage performs long-context activation with
integrated higher-quality mid-training data, sequentially extending
context length via YaRN [@peng2023yarn] interpolation. This yields
significant generalization improvements in long-context text
understanding and long video comprehension.

## Post-Training

### Supervised Fine-Tuning

Following the SFT pipeline established by Kimi K2 [@team2025kimik2], we
developed K2.5 by synthesizing high-quality candidate responses from K2,
K2 Thinking and a suite of proprietary in-house expert models. Our data
generation strategy employs specialized pipelines tailored to specific
domains, integrating human annotation with advanced prompt engineering
and multi-stage verification. This methodology produced a large-scale
instruction-tuning dataset featuring diverse prompts and intricate
reasoning trajectories, ultimately training the model to prioritize
interactive reasoning and precise tool-calling for complex, real-world
applications.

### Reinforcement Learning

Reinforcement learning constitutes a crucial phase of our post-training.
To facilitate joint optimization across text and vision modalities, as
well as to enable PARL for agent swarm, we develop a Unified Agentic
Reinforcement Learning Environment
(Appendix [\[app:rl_infra\]](#app:rl_infra){reference-type="ref"
reference="app:rl_infra"}) and optimize the RL algorithms. Both
text-vision joint RL and PARL are built upon the algorithms described in
this section.

#### Policy Optimization

For each problem $x$ sampled from a dataset $\mathcal{D}$, $K$ responses
$\{y_1,\dots,y_K\}$ are generated using the previous policy
$\pi_{\mathrm{old}}$. We optimize the model $\pi_\theta$ with respect to
the following objective: $$\begin{align}
L_{\mathrm{RL}}(\theta) = \mathbb{E}_{x \sim\mathcal{D}}
\left[ \frac{1}{N} \sum_{j=1}^K \sum_{i=1}^{|y_j|}
\mathrm{Clip}
\left(
\frac{\pi_{\theta}(y_j^i | x, y_j^{0:i})}{\pi_{\mathrm{old}}(y_j^i | x, y_j^{0:i}) }, \alpha, \beta
\right)
({r}(x, y_j) - \bar{r}(x))- \tau \left( \log \frac{\pi_{\theta}(y_j^i | x, y_j^{0:i})}{\pi_{\mathrm{old}}(y_j^i | x, y_j^{0:i}) } \right)^2
\right]
\, .
\label{eq:rl-objective}
\end{align}$$ Here $\alpha, \beta, \tau >0$ are hyperparameters,
$y^j_{0:i}$ is the prefix up to the $i$-th token of the $j$-th response,
$N=\sum_{i=1}^{K} |y_i|$ is the total number of generated tokens in a
batch, $\bar{r}(x) = \frac{1}{K}\sum_{j=1}^K r(x, y_j)$ is the mean
reward of all generated responses.

This loss function departs from the policy optimization algorithm used
in K1.5 [@team2025kimi] by introducing a token-level clipping mechanism
designed to mitigate the off-policy divergence amplified by
discrepancies between training and inference frameworks. The mechanism
functions as a simple gradient masking scheme: policy gradients are
computed normally for tokens with log-ratios within the interval
$[\alpha, \beta]$, while gradients for tokens falling outside this range
are zeroed out. Notably, a key distinction from standard PPO clipping
[@schulman2017proximal] is that our method relies strictly on the
log-ratio to explicitly bound off-policy drift, regardless of the sign
of the advantages. This approach aligns with recent strategies proposed
to stabilize large-scale RL training [@yao2025offpolicy; @IcePop2025].
Empirically, we find this mechanism essential for maintaining training
stability in complex domains requiring long-horizon, multi-step tool-use
reasoning. We employ the MuonClip
optimizer [@jordan2024muon; @liu2025muon] to minimize this objective.

#### Reward Function

We apply a rule-based outcome reward for tasks with verifiable
solutions, such as reasoning and agentic tasks. To optimize resource
consumption, we also incorporate a budget-control reward aimed at
enhancing token efficiency. For general-purpose tasks, we employ
Generative Reward Models (GRMs) that provide granular evaluations
aligned with Kimi's internal value criteria. In addition, for visual
tasks, we design task-specific reward functions to provide fine-grained
supervision. For visual grounding and point localization tasks, we
employ an F1-based reward with soft matching: grounding tasks derive
soft matches from Intersection over Union (IoU) and point tasks derive
soft matches from Gaussian-weighted distances under optimal matching.
For polygon segmentation tasks, we rasterize the predicted polygon into
a binary mask and compute the segmentation IoU against the ground-truth
mask to assign the reward. For OCR tasks, we adopt normalized edit
distance to quantify character-level alignment between predictions and
ground-truth. For counting tasks, rewards are assigned based on the
absolute difference between predictions and ground-truth. Furthermore,
we synthesize complex visual puzzle problems and utilize an LLM verifier
(Kimi K2) to provide feedback.

#### Generative Reward Models

Kimi K2 leverages a self-critique rubric reward for open-ended
generation [@team2025kimik2], and K2.5 extends this line of work by
systematically deploying *Generative Reward Models (GRMs)* across a
broad range of agentic behaviors and multimodal trajectories. Rather
than limiting reward modeling to conversational outputs, we apply GRMs
on top of verified reward signals in diverse environments, including
chat assistants, coding agents, search agents, and artifact-generating
agents. Notably, GRMs function not as binary adjudicators, but as
fine-grained evaluators aligned with Kimi's values that are critical to
user experiences, such as helpfulness, response readiness, contextual
relevance, appropriate level of detail, aesthetic quality of generated
artifacts, and strict instruction following. This design allows the
reward signal to capture nuanced preference gradients that are difficult
to encode with purely rule-based or task-specific verifiers. To mitigate
reward hacking and overfitting to a single preference signal, we employ
multiple alternative GRM rubrics tailored to different task contexts.

## Training Infrastructure

Kimi K2.5 inherits the training infrastructure from Kimi
K2 [@team2025kimik2] with minimal modifications. For multimodal
training, we propose Decoupled Encoder Process, where the vision encoder
is incorporated into the existing pipeline with negligible additional
overhead.

### Decoupled Encoder Process (DEP)

In a typical multimodal training paradigm utilizing Pipeline Parallelism
(PP), the vision encoder and text embedding are co-located in the first
stage of the pipeline (Stage-0). However, due to the inherent variations
of multimodal input size (e.g., image counts and resolutions), Stage-0
suffers from drastic fluctuations in both computational load and memory
usage. This forces existing solutions to adopt custom PP configurations
for vision-language models --- for instance, [@team2025kimivl] manually
adjusts the number of text decoder layers in Stage-0 to reserve memory.
While this compromise alleviates memory pressure, it does not
fundamentally resolve the load imbalance caused by multimodal input
sizes. More critically, it precludes the direct reuse of parallel
strategies that have been highly optimized for text-only training.

Leveraging the unique topological position of the visual encoder within
the computation graph --- specifically, its role as the start of the
forward pass and the end of the backward pass --- our training uses
**Decoupled Encoder Process (DEP)**, which is composed of three stages
in each training step:

- **Balanced Vision Forward:** We first execute the forward pass for all
  visual data in the global batch. Because the vision encoder is small,
  we replicate it on all GPUs regardless of other parallelism
  strategies. During this phase, the forward computational workload is
  evenly distributed across all GPUs based on load metrics (e.g., image
  or patch counts). This eliminates load-imbalance caused by PP and
  visual token counts. To minimize peak memory usage, we discard all
  intermediate activations, retaining only the final output activations.
  The results are gathered back to PP Stage-0;

- **Backbone Training:** This phase performs the forward and backward
  passes for the main transformer backbone. By discarding intermediate
  activations in the preceding phase, we can now fully leverage any
  efficient parallel strategies validated in pure text training. After
  this phase, gradients are accumulated at the visual encoder output;

- **Vision Recomputation & Backward:** We re-compute the vision encoder
  forward pass, followed by a backward pass to compute gradients for
  parameters in the vision encoder;

DEP not only achieves load-balance, but also decouples the optimization
strategy of the vision encoder and the main backbone. K2.5 seamlessly
inherits the parallel strategy of K2, achieving a multimodal training
efficiency of 90% relative to text-only training. We note a concurrent
work, LongCat-Flash-Omni [@team2025longcat], shares a similar design
philosophy.
