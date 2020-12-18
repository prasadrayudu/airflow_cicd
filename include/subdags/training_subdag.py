from airflow.models import DAG, Variable
from airflow.operators.papermill_operator import PapermillOperator

def subdag_factory(parent_dag_name, child_dag_name, default_args):
    with DAG(dag_id=f'{parent_dag_name}.{child_dag_name}', default_args=default_args) as dag:

        model_settings = Variable.get('avocado_dag_model_settings', deserialize_json=True)

        for feature in model_settings['max_features']:
            for estimator in model_settings['n_estimators']:
                ml_id = feature + '_' + str(estimator)
                PapermillOperator(
                    task_id=f'training_model_{ml_id}',
                    input_nb='/usr/local/airflow/include/notebooks/avocado_prediction.ipynb',
                    output_nb=f'/tmp/out-model-avocado-prediction-{ml_id}.ipynb',
                    parameters={
                        'filepath': '/tmp/avocado.csv',
                        'n_estimators': estimator,
                        'max_features': feature,
                        'ml_id': ml_id
                    },
                    pool='training_pool'
                )

        return dag