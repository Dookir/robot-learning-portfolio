# Attribution

This portfolio summarizes reproduction and integration work. It does not distribute the external systems below or claim authorship of their underlying models and methods.

## Vision language action models

- [FluxVLA-Tron2](https://github.com/clearlab-sustech/FluxVLA-Tron2): task/runtime baseline used for the reproduction.
- [FluxVLA](https://github.com/FluxVLA/FluxVLA): upstream VLA implementation.
- [OpenPI](https://github.com/Physical-Intelligence/openpi): PI0.5-related model implementation.
- [LeRobot](https://github.com/huggingface/lerobot): recording/data-format tooling.

## Dexterous hand work

Revo3 vendor materials provide robot kinematics, models and original alignment/IK. MANO supplies the human-hand representation used in the retargeting work. Lab C2Dex-related implementation and the contact-preservation method are external foundations, rather than newly proposed algorithms in this portfolio. HORA, REGRIND and OriginData are source data contexts, not datasets released here.

No vendor code, robot/object mesh, MANO asset, recorded dataset sample, inferred source trajectory or restricted dataset package is included. Dataset names and selected scalar experiment summaries are used to identify the work discussed; naming them does not confer data access or redistribution rights.

## Simulation and learning software

- [MuJoCo](https://github.com/google-deepmind/mujoco)
- [Gymnasium](https://github.com/Farama-Foundation/Gymnasium)
- [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3)
- [ROS 2](https://github.com/ros2)

The public links identify upstream projects. Their current releases need not match the historical experiment environment. See each project's own licensing and citation instructions when using that software; the MIT license here applies only to the original portfolio material.
