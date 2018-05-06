Sample project-template for `React + Typescript + Parcel + Flask`.

- Client: React + Typescript; building with parcel
- Server: Python Web Server(Flask)
- Both client and server include several other modules too.

# How to Build and Run

```bash
# Preparation (install modules)
pipenv install
cd client && yarn install && cd ..

# Compile and build client (Typescript and React)
cd client && yarn build && cd ..

# Run server
pipenv run python3 app.py
```

# Use Hot-Load-Module mode

After executing the fllowing commands, whenever you modify client/server source codes, it'll be automatically rebuild and reload.

```bash
# You should prepare two terminals.

# Terminal-1: Run server
pipenv run python3 app.py

# Terminal-2: Run realtime build (watch mode)
cd client
yarn watch
```
