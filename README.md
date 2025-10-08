# SLAM - Simultaneous Localization and Mapping

A Python implementation of SLAM (Simultaneous Localization and Mapping) algorithms for robotics applications. This project provides tools for robot localization and environment mapping using sensor data.

## Overview

This repository contains a complete SLAM implementation with data processing pipelines, visualization tools, and utilities for real-time mapping and localization. It's designed for autonomous navigation systems and robotics research.

## Features

- Real-time simultaneous localization and mapping
- Support for various sensor inputs (LiDAR, cameras, IMU)
- Data preprocessing and filtering modules
- Map visualization and export capabilities
- Particle filter and EKF-based implementations
- Sensor fusion for improved accuracy
- Modular architecture for easy customization

## Tech Stack

- **Python 3.x** - Primary programming language
- **NumPy** - Numerical computing
- **Matplotlib** - Data visualization
- **OpenCV** - Computer vision (if applicable)
- **SciPy** - Scientific computing

## Project Structure

```
.
├── src/
│   ├── slam.py              # Main SLAM algorithm implementation
│   ├── localization.py      # Localization modules
│   ├── mapping.py           # Mapping algorithms
│   ├── sensors.py           # Sensor data processing
│   └── utils.py             # Utility functions
├── data/                    # Sample data and datasets
├── tests/                   # Unit tests
├── notebooks/               # Jupyter notebooks for analysis
└── requirements.txt         # Python dependencies
```

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BM-45/slam.git
cd slam
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic SLAM Execution

```python
from src.slam import SLAM
from src.sensors import SensorData

# Initialize SLAM system
slam = SLAM()

# Load sensor data
data = SensorData('data/sample.bag')

# Run SLAM algorithm
for measurement in data:
    slam.update(measurement)
    map, pose = slam.get_state()
```

### Visualization

```python
from src.utils import visualize_map

# Visualize the generated map
visualize_map(slam.get_map(), slam.get_trajectory())
```

### Command Line Interface

```bash
# Run SLAM on a dataset
python src/slam.py --input data/dataset.bag --output results/

# Enable visualization
python src/slam.py --input data/dataset.bag --visualize
```

## Algorithms Implemented

- **FastSLAM** - Particle filter-based SLAM
- **EKF-SLAM** - Extended Kalman Filter SLAM
- **Grid Mapping** - Occupancy grid-based mapping
- **Feature-based SLAM** - Landmark detection and tracking


