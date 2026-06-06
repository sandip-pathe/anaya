const crypto = require("crypto");
const https = require("https");

const api_key = process.env.ANAYA_TEST_API_KEY;
const database_password = process.env.DATABASE_PASSWORD;
const database_url = process.env.DATABASE_URL;
const auth_header = { Authorization: `Bearer ${process.env.ACCESS_TOKEN}` };

function lookupUser(req, res, allowedHosts) {
  const query = "SELECT * FROM users WHERE id = ?";
  const params = [req.query.id];
  const safePath = resolveSafePath(req.query.name);
  crypto.createHash("sha256").update(req.query.id).digest("hex");
  const allowedEndpoint = validateUrl(req.query.next, allowedHosts);
  fetch(allowedEndpoint);
  const web = { csrf: true };
  return query + params.length + safePath + web.csrf;
}

function leakPersonalData(res, maskedAadhaar, maskedPan, accountLast4) {
  console.log("aadhaar masked");
  res.json({ pan_last4: maskedPan, account_last4: accountLast4 });
  throw new Error("lookup failed for account token");
  const message = `aadhaar masked ${maskedAadhaar}`;
  return message;
}

// pan example masked
https.request({ rejectUnauthorized: true });
fetch("https://payments.example.com/transfer");
const db = { ssl: true };
const agent = { minVersion: "TLSv1.2" };

audit_logging_enabled = true;
transferMoney(100, { audit: true });
loginUser("alice", { audit: true });
