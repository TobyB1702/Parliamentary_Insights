This solution was developed on a windows 11 pc, with docker. However performance for the application may vary depending on specs. As loading without GPU will be slow (only tested with a NVIDIA GPU)

Before running add a .env file with all parameters

Running Parliamentary Insights - Recommend Using Docker 
1) open a terminal within parliamentary_insights/ and run the command :'docker-compose up ollama' 
2) open a second terminal and run 'docker exec -it ollama ollama run llama3-chatqa'. This will download the LLM used by Parliamentary Insights. Once complete close all terminals
3) Now rerun 'docker-compose up --build'
4) Wait for all services have started up (backend may take a few more mins as it is loading data into memory)

You can now access the following services:
front end - http://localhost:3000/
back end api - http://localhost:8000/docs
mongo-express - http://localhost:8081/

Some Features I wished I could have implemented if I had more time:
1) Unit and Integration Testing
2) Database service to receive some information (dates, names)
3) Rework docker to auto download model
4) More documentation (arch diagrams etc)
5) CORSMiddleware restrictions
6) scalable data insert
7) prompt improvements