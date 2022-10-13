# Matrix Moderation Tool

This program (a matrix bot) allows you to protect your moderated rooms from cryptocurrency freaks and other spammers. The program uses a Bayesian antispam classifier to filter messages.

## What dependencies are required?

This program requires **python** and the following libraries installed:

- [antispam](https://github.com/dinever/antispam)
- [matrix-nio](https://github.com/poljar/matrix-nio)

Both of the libraries can be installed by **pip**.

## How to install and run the bot?

Open a Terminal and type (or copy / paste) the following commands in:

```bash
pip install antispam matrix-nio
git clone https://github.com/insreset/Matrix-Moderation-Tool.git
cd Matrix-Moderation-Tool
python3 main.py
```

Create a new matrix account with moderator privileges in your room(s) and enter the credentials.

## Contact

Feel free to contact [me](https://matrix.to/#/@rfe:matrix.org) with any questions!
