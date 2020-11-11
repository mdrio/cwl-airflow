#! /usr/bin/env python3
import json

from airflow.operators.subdag_operator import SubDagOperator
from airflow.utils.decorators import apply_defaults

from cwl_airflow.utilities.cwl import collect_reports
from cwl_airflow.utilities.report import post_status


class CWLSubOperator(SubDagOperator):


    @apply_defaults  # in case someone decided to overwrite default_args from the DAG
    def __init__(
        self,
        task_id,
        subdag,
        *args, **kwargs
    ):
        super().__init__(task_id=task_id, subdag=subdag, *args, **kwargs)


    def execute(self, context):
        """
        Creates job from collected reports of all finished tasks in a parent DAG.
        Then triggers subdag. Writes report file location to X-Com.
        """

        post_status(context)

        job_data = collect_reports(context)

        execution_date = context["execution_date"]
        self.subdag.run(
            start_date=execution_date,
            end_date=execution_date,
            donot_pickle=True,
            executor=self.executor,
            conf={"job": job_data}
        )
        
        results_location = context["ti"].xcom_pull(task_ids="CWLJobGatherer")
        with open(results_location, "r") as input_stream:
            return json.load(input_stream)