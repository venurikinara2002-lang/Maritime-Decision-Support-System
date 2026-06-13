# ⚓ Maritime Decision Support System: OceanGuard Optimizer

Offshore fisheries represent a vital sector in the maritime economy, yet they face high operational risks and significant capital investments. The **Maritime Decision Support System (OceanGuard Optimizer)** is an interactive Streamlit-based web application designed to bridge the gap between traditional fishing knowledge and predictive data science.

By analyzing historical fleet data from **20,000+ Sri Lankan offshore fishing trip records**, this system provides fishermen and ship owners with real-time safety testing, pre-trip cost estimation, species catch distribution analysis, and profit break-even calculations.

---

## 📽️ Application Demonstration Video
To see the system in action and explore its capabilities, view our interactive walkthrough:
👉 **[Watch the App Demonstration Video](https://drive.google.com/file/d/1JGMckStJ79ISPMJ0zjQ_V_vEWACapX18/view?usp=sharing)**

---

## 🚀 Key Modules & Features

The application is structured into three primary stations accessible via the **Navigation Center** sidebar:

### 1. ⚓ Fleet Operations Dashboard
An introductory station that provides an overview of the fleet and real-time safety evaluation.
* **Key Fleet Metrics**: Displays high-level KPIs including **Total Vessels**, **Average Fuel Cost (LKR)**, **Average Crew Size**, and **Average Trip Days** based on historical records.
* **Live Sea Safety Tester**: An interactive form utilizing sliders for **Wind Speed (kph)** and **Wave Height (m)**. It evaluates immediate sea conditions:
  * 🟢 **Calm Status**: Wave < 1.0m & Wind < 15kph — **Safe to Depart**
  * 🟡 **Moderate Status**: Wave 1.0m–2.0m or Wind 15–30kph — **Proceed with Caution**
  * 🔴 **Rough Status**: Wave > 2.0m or Wind > 30kph — **Departure Not Recommended**
* **Historical Distribution**: A dynamic pie chart highlighting the selected sea safety level and comparing it with historical fleet patterns.

### 2. 📊 Fleet Risk & Catch Analysis
A data exploration dashboard showcasing the relationship between vessel configuration, safety rating, and species catches.
* **Historical Safety Ratings**: Visual breakdown of safety category distributions of past voyages.
* **Crew Size vs. Cost**: Analysis of how operational costs scale relative to the size of the crew.
* **Species Weight Distribution**: Interactive histogram showing the catch weights (kg) for key target species (**Yellowfin Tuna**, **Skipjack**, and **Marlin**).

### 3. 💳 Pre-Trip Financial Optimizer
A predictive tool that applies Machine Learning models to optimize voyage finances.
* **Trip Cost Estimator**: Uses a trained **Random Forest Regressor** to predict a voyage's total operational cost (in LKR) based on vessel specifications (Engine HP, Crew Size, Trip Distance, allowed Offshore Days) and expected weather conditions (Wind, Waves).
* **Break-Even Catch targets**: Calculates the minimum required mixed species catch (in kg) to cover the estimated operational expenses. User-defined market rates can be adjusted for Yellowfin, Skipjack, and Marlin.
* **Fisherman Alert Alerting**: Generates a custom visual callout flagging the precise catch threshold needed to ensure profitability.

---

## 🛠️ Tech Stack & Model Details

* **Interface**: Streamlit (with customized navy-blue maritime styling & UI controls)
* **Programming**: Python
* **Machine Learning**: Scikit-Learn `RandomForestRegressor`
* **Data Manipulation**: Pandas, NumPy
* **Visualization**: Matplotlib, Seaborn

---

## 📁 Repository Structure
```
├── final/
│   ├── app.py                  # Main Streamlit application source code
│   ├── boat_dashboard.png      # Application dashboard visual banner
│   └── fishing_data.csv        # Preprocessed historical trip dataset
├── Demonstration.mp4           # Local app video file
├── Individual Contribution Report .pdf  # Academic/project contribution report
├── collabfile.ipynb            # Jupyter notebook detailing modelling workflow
└── README.md                   # Project documentation
```

---

## 💻 How to Install & Run Locally

Follow these steps to run the OceanGuard Optimizer application on your local machine:

### Prerequisite
Ensure you have Python 3.8+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/venurikinara2002-lang/Maritime-Decision-Support-System.git
cd Maritime-Decision-Support-System
```

### 2. Install Required Libraries
Install all necessary dependencies:
```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### 3. Run the Streamlit Application
Start the Streamlit server from the root directory:
```bash
streamlit run final/app.py
```

Open the local URL provided in your terminal (typically `http://localhost:8501`) to interact with the system.

---
*Developed as part of the Fisheries Project App analytics solution.*
