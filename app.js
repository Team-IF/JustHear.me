const express = require("express");
const config = require('./config/config');
const app = express();
const router = require('./router/main')(app);

app.use((req, res, next) => {
    console.log(`${req.connection.remoteAddress} : ${req.path}`);
    next();
});

app.use('/test', require('./routes/test'));

//오류남
//const router = require('./router/main')(app);

const server = app.listen(config.port, config.host, () => console.log(`Listening on port ${config.port}...`));
