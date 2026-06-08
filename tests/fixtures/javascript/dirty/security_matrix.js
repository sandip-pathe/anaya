const child_process = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const https = require("https");

const api_key = "anaya_test_secret_1234567890";
const database_password = "super-secret-password";
const database_url = "postgresql://billing:BillingPass123@db.internal:5432/app";
const aws_access_key = "ANAYA_FAKE_AWS_KEY_PLACEHOLDER";
const private_key_header = "ANAYA_FAKE_PRIVATE_KEY_HEADER";
const auth_header = { Authorization: "Bearer abcdefghijklmnopqrstuvwxyz123456" };

function lookupUser(req, res) {
  const query = `SELECT * FROM users WHERE id = ${req.query.id}`;
  child_process.exec("sh -c " + req.query.cmd);
  eval(req.query.expr);
  fs.readFile("../exports/" + req.query.name, "utf8", () => {});
  crypto.createHash("md5").update(req.query.id).digest("hex");
  fetch(req.query.url);
  const web = { csrf: false };
  return query + web.csrf;
}

function leakPersonalData(res, aadhaarNumber, panNumber, accountNumber, cvv) {
  console.log(`aadhaar ${aadhaarNumber}`);
  res.json({ pan: panNumber, cvv });
  throw new Error(`account_number ${accountNumber}`);
}

// pan: ABCDE1234F
const message = `aadhaar ${aadhaarNumber}`;

https.request({ rejectUnauthorized: false });
fetch("http://payments.example.com/transfer");
const db = { ssl: false };
const agent = { minVersion: "TLSv1.1" };

audit_logging_enabled = false;
transferMoney(100, { skip_audit: true });
loginUser("alice", { audit: false });
