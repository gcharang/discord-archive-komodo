#!/usr/bin/env sh

# abort on errors
set -e


# build
docker build -t komodo_discord_archive_docs_image .
docker run --rm -v $(pwd):/app/ -w /app/ -u $(id -u):$(id -g) komodo_discord_archive_docs_image



# navigate into the build output directory
cd docs/.vuepress/dist

# if you are deploying to a custom domain
#echo 'discord.komodo.lordofthechains.com' > CNAME

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io
# git push -f git@github.com:<USERNAME>/<USERNAME>.github.io.git master

# if you are deploying to https://<USERNAME>.github.io/<REPO>
GIT_USER=$(git config --global user.name)
git push -f git@github.com:$GIT_USER/discord-archive-komodo.git master:gh-pages

cd -
