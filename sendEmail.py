import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def main():
    # Paramètres
    sender_email = "pierrechem1@gmail.com"
    receiver_email = "pierre.chemin@groupe-cyllene.com"
    password = "yfwr rcat wdwk covw"

    # Créer un objet MIMEMultipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Rapport scann DarkWeb"

    # Corps du message
    body = "Bonjour messieurs,\n\nVous trouverez ci-joint le rapport généré lors du scan du Dark web.\n\Cordialement,\nChef des robots"
    message.attach(MIMEText(body, "plain"))

    # Attachement du fichier texte
    filename = "result/dataFound.txt"
    with open(filename, "r") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part)

    # Créer une connexion SMTP sécurisée avec le serveur Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(message)

    print("E-mail envoyé avec succès")

if __name__ == "__main__":
    main()