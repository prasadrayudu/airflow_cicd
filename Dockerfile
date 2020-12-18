FROM astronomerinc/ap-airflow:1.10.12-buster-onbuild

ENV AIRFLOW_VAR_AVOCADO_DAG_MODEL_SETTINGS='{"max_features":["auto", "sqrt"], "n_estimators": [100, 150]}'