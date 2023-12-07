# DS223-Marketing-Analytics-Group-Project-Group2

## CLTV Analysis Package

This Python package, CLTVModel, helps retail businesses understand and optimize Customer Lifetime Value (CLTV). It handles tasks like loading data, doing calculations, using predictive models, and providing insights for smarter decisions.

In order to use the package, you should follow these steps
1- Install the package (pip install clv-analysis-package)
2- Import the Package(from cltv_analysis_package import CLTVModel)
3- Instantiate CLTVModel 

 Use Case 1: CLV Analysis
cltv_model = CLTVModel()
cltv_model.load_data()

Use case 2: Predictive Model
cltv_model_with_predictive = CLTVModel(use_predictive_model=True)
cltv_model_with_predictive.load_data()

4- Obtain Results
CLV Analysis:
segments_summary = cltv_model.display_segments_summary()
print(segments_summary)

Predictive Model:
cltv_predictions = cltv_model_with_predictive.predict_cltv()
print(cltv_predictions)
