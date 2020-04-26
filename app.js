const express = require("express");
const app = express();
const router = require('./router/main')(app);

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));
