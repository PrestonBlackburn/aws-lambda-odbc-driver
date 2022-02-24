#FROM public.ecr.aws/lambda/python:3.9
FROM prestonbl/aws-lambda-python-with-sqlserver-odbc-driver

ADD requirements.txt .
ADD app.py ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir --upgrade pip setuptools \ 
    && pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
