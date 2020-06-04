FROM python:3.7
COPY . /docker_app
WORKDIR /docker_app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000 
CMD ["python", "app/webapp.py", "-t", "blended_skill_task", "-mf", "zoo:blender/blender_90M/model"]
