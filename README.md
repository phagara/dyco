# dyco

a silly discord bot

## development

tech used:
  * latest python 3.x (`python:3-alpine` docker image)
  * discord.py https://discordpy.readthedocs.io/en/latest/

### test your changes

#### first time setup

  * go to https://discordapp.com/developers/applications
  * create a new app profile
  * follow [get the bot auth token from discord](#get-the-bot-auth-token-from-discord) to get `<TOKEN>`
  * `echo 'token: <TOKEN>' > ~/.dycorc`
  * manually invite the bot to your testing server https://discordpy.readthedocs.io/en/latest/discord.html#inviting-your-bot

#### run the bot

```bash
python3 -m dyco
```

### merge changes

never not force-push to master

### publish a versioned release

  * create release at https://github.com/phagara/dyco/releases
  * github actions workflow "release" is triggered
  * new container build appears at https://github.com/phagara/dyco/packages

## deploy to production

### prerequisites

  * running k8s cluster
  * `kubectl` configured to communicate with the cluster
  * discord app profile created (https://discordapp.com/developers/applications)

### k8s secrets provisioning

#### get the bot auth token from discord

Where to find the auth token:

  * go to https://discordapp.com/developers/applications
  * select the bot app under "applications"
  * select "bot" from the menu
  * "click to reveal token"

From now on, this piece of data is referred to as `<TOKEN>`.

#### convert token to base64

Kubernetes requires secrets to be base64 encoded, so do eg.:

```bash
echo -n '<TOKEN>' | base64 -w0
```

From now on, this is `<TOKEN_BASE64>`.

#### create secret yaml

Create a file with the following contents:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dyco-secrets
type: Opaque
data:
  DYCO_TOKEN: <TOKEN_BASE64>
```

This file is referred to as `<DYCO_SECRETS_FILE>`.

#### apply the bot token secret to k8s cluster

```bash
kubectl apply -f <DYCO_SECRETS_FILE>
```

#### create github token for registry auth

  * go to https://github.com/settings/tokens
  * click "create new token"
  * enter some note to help you identify this token
  * tick the "repo" and "read:packages" checkboxes
  * confirm by pressing the big green button at the bottom

Copy the secret token shown, this is your `<GH_TOKEN>`.

#### apply github docker registry creds to k8s cluster

Replace `<GH_USER>` with your Github username,
`<GH_EMAIL>` with the associated e-mail address
and `<GH_TOKEN>` with the value from previous step.

```bash
kubectl create secret docker-registry dyco-registry-creds --docker-server=docker.pkg.github.com --docker-username=<GH_USER> --docker-password=<GH_TOKEN> --docker-email=<GH_EMAIL>
```

### deploy dyco

```bash
kubectl apply -f k8s-manifest-dyco.yml
```

### keep dyco up-to-date

simply restart the deployment, it is configured to always pull the `:latest` image:

```bash
kubectl rollout restart deployment dyco
```