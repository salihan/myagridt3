# MyAgriDt

This project aims to develop a plant growth monitoring dashboard using Python and Streamlit. The dashboard provides descriptive analytics for plant growth monitoring and offers predictive analytics for interventions to achieve yield targets.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Plant Growth Monitoring Dashboard is a web application built using Streamlit, a Python library for creating interactive web apps. The main purpose of this dashboard is to monitor the growth of plants and provide insights through descriptive analytics. Additionally, it offers predictive analytics to suggest interventions required to achieve yield targets.

## Features

- Descriptive Analytics:
  - Visualize plant growth data using charts and graphs.
  - Display key metrics related to plant growth, such as height, weight, and nutrient levels.
  - Generate reports on plant growth patterns and trends.

- Predictive Analytics:
  - Analyze historical plant growth data to predict future growth patterns.
  - Recommend interventions, such as adjusting nutrient levels or providing additional light, to achieve desired yield targets.

- MVC Structure:
  - The project follows the Model-View-Controller (MVC) architectural pattern.
  - The Model handles the data processing and analytics, including descriptive and predictive tasks.
  - The View presents the visualizations and user interface using Streamlit.
  - The Controller manages the interaction between the Model and View, ensuring data flow and functionality.

## Installation

To set up the Plant Growth Monitoring Dashboard on your local machine, follow these steps:

1. Clone the repository:
    git clone https://github.com/salihan/myagridt3.git
2. Install the required dependencies:
    pip install -r requirements.txt
3. Run the application: streamlit run app.py


The application will be accessible at `http://localhost:8501` in your web browser.

## Usage

Once the application is running, you can interact with the Plant Growth Monitoring Dashboard using your web browser. Explore the different sections of the dashboard to view descriptive analytics and make use of the predictive analytics features to achieve yield targets.

## Folder Structure

The project's folder structure is organized as follows:

- `app.py`: The main application file that initializes the Streamlit app and connects the Model and View components.
- `models/`: Contains the modules responsible for data processing, descriptive analytics, and predictive analytics.
- `views/`: Includes the Streamlit scripts that define the different pages and visualizations for the dashboard.
- `datasets/`: Includes datasets for the Model component.

## Contributing

Contributions to the Plant Growth Monitoring Dashboard project are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).



