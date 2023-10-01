# PokeDB

## Description
- Look up Pokemon from the original Kanto region
- Find out their type, height, weight, and more!
- Find items and their descriptions
- Add Pokemon to your team, up to six.
- Built in caching to speed up the app

## Filling the Database
- To fill the database:
  - Click the button that says "Fill Database"
  - Please note it will take a bit to complete. When it's done you'll get a message saying data filled.

## Now with Docker!
- To run the app with docker, run the following commands:
  - `docker build -t pokedex .`
  - `docker run -p 5000:5000 pokedex`
- To run the app with docker-compose, run the following commands:
  - `docker-compose build`
  - `docker-compose up`

## And DevOps!
- If you have portainer or another docker management system that allows you to use github repos, you can point to this repo and use `dc-ops.yml` to deploy the app. 
- You can also look at the `dc-swarm.yml` file to see how to deploy the app to a swarm. This will create one redis and postgres instance with three replicas of the app.
### Thank you
- Thank you to @digitsgaming for the continual support with server infrastructure and deployment.