const express = require("express");
const morgan = require("morgan");

const HttpError = require("./models/httperror");
const MongoClient = require('mongodb').MongoClient;

const config = require('./configurator').config();

const app = express();
let httpServer;
let dbClient;

async function init() {
    console.log("Connecting DB...");

    dbclient = new MongoClient(config.dburl, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
    await dbclient.connect();
    app.locals.db = dbclient.db(config.dbname);
    app.locals.config = config;

    console.log("Loading Modules...");

    // logger
    app.use(morgan({
        format: "short",
        stream: {
            write: (str) => {
                console.log(str);
            }
        }
    }));

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

    httpServer = app.listen(config.port, config.host, () => console.log(`Listening on port ${config.port}...`));

    // send ready signal to PM2 (Process Manager)
    try {
        process.send('ready');
    } catch (e) {
        console.log(e);
    }
};

async function stopServer() {
    console.log("Stopping server");

    dbClient.close();
    httpServer.close();

    console.log("Stopped");
}

// process exit signal
process.on('SIGINT', function () {
    stopServer();
});

init();