const express = require("express");

const HttpError = require("./routes/httperror").HttpError;
const MongoClient = require('mongodb').MongoClient;

const config = require('./config/config');
const app = express();

async function init() {
    let dburl = `mongodb://${config.db.user}:${config.db.password}@${config.db.hostname}/${config.db.dbname}?authSource=admin&authMechanism=SCRAM-SHA-1`;
    let dbclient = new MongoClient(dburl, { useNewUrlParser: true });
    await dbclient.connect();
    const db = dbclient.db(config.db.dbname);

    // test logger
    app.use((req, res, next) => {
        console.log(`${req.connection.remoteAddress} : ${req.path}`);
        next();
    });

    app.use('/auth', require('./routes/auth')(db));
    app.use('/test', require('./routes/test')(db));

    // error handler
    app.use((err, req, res, next) => {
        let status = 500;
        let message = "internal server error";

        if (err instanceof HttpError) {
            status = err.status;
            message = err.message;
        }
        else if (err instanceof Error) {
            message = `${err.name}: ${err.message}`;
        }

        console.log(err);

        res.status(status)
            .send({
                result: false,
                status: status,
                message: message
            });
    });

    const httpServer = app.listen(config.port, config.host, () => console.log(`Listening on port ${config.port}...`));
};

init();