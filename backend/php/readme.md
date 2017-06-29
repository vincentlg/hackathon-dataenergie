> Laravel 5.3 project

## Project Setup (With Docker)
```bash
# clone the project
git clone ??

# Install dependencies
docker run --rm -v $(pwd):/app composer/composer install

# Starting the services
docker-compose up

# Environment configuration file
cp .env.example .env

# Application key & optimize
docker-compose exec app php artisan key:generate
docker-compose exec app php artisan optimize

# database + seed
docker-compose exec app php artisan migrate --seed

# app root
http://0.0.0.0:8080


# kill project
docker-compose kill

#python 
Install anaconda for python 

``https://docs.continuum.io/anaconda/install/linux``
