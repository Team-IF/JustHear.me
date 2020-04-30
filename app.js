const express = require("express");

const HttpError = require("./models/httperror").HttpError;
const MongoClient = require('mongodb').MongoClient;

const config = require('./config/config');
const app = express();

async function init() {
    console.log("Connecting DB...");

    let dburl = `mongodb://${config.db.user}:${config.db.password}@${config.db.hostname}/${config.db.dbname}?authSource=admin&authMechanism=SCRAM-SHA-1`;
    let dbclient = new MongoClient(dburl, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
    await dbclient.connect();
    app.locals.db = dbclient.db(config.db.dbname);
    app.locals.config = config;

    console.log("Loading Modules...");

    // test logger
    app.use((req, res, next) => {
        console.log(`${req.connection.remoteAddress} : ${req.path}`);
        next();
    });

    app.use('/auth', require('./routes/auth'));
    app.use('/profile', require('./routes/profile'));
    app.use('/test', require('./routes/test'));

    // error handler
    app.use((err, req, res, next) => {
        let status = 500;
        let message = '';

        if (err instanceof HttpError) {
            status = err.status;
            message = err.message;
        }
        else if (err instanceof Error) {
            message = `${err.name}: ${err.message}`;
        }

        if (!message || config.product)
            message = 'internal server error';

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

console.log("start JustHear.me server");
init();