const express = require("express");
const nodemailer = require("nodemailer");
const multer = require("multer");
const path = require("path");

const app = express();
const port = process.env.PORT || 3000; // Choose the desired port

// Nodemailer transporter
const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "dev.omari.ai@gmail.com",
    pass: "pvag lwwq csgo qena",
  },
});

// Multer configuration for handling file uploads
const storage = multer.memoryStorage();
const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // Limit the file size to 5MB
});

// Function to send email with attached PDF
const sendEmailWithAttachment = (email, pdfBuffer) => {
  const mailOptions = {
    from: "dev.omari.ai@gmail.com",
    to: email,
    subject: "Finclan Community Invite",
    text: "Please find attached PDF",
    attachments: [
      {
        filename: "invitation.pdf",
        content: pdfBuffer,
      },
    ],
  };

  // Send the email
  transporter.sendMail(mailOptions, (err, info) => {
    if (err) {
      console.error(err);
      return false;a
    }
    console.log("Email sent:", info.response);
    return true;
  });
};

// Express route to handle POST request with PDF and email
app.post("/send-email-with-attachment", upload.single("pdf"), (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).send("Email is required");
  }

  const pdfBuffer = req.file.buffer;

  if (!pdfBuffer) {
    return res.status(400).send("PDF file is required");
  }

  const emailSent = sendEmailWithAttachment(email, pdfBuffer);

  if (emailSent) {
    res.status(200).send("Email with attachment sent successfully");
  } else {
    res.status(500).send("Failed to send email with attachment");
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
