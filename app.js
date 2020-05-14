const express = require('express');
const morgan = require('morgan');

const HttpError = require('./models/httperror');
const mongoose = require('mongoose');

const config = require('./configurator').config();

const app = express();
let httpServer;
let dbClient;

async function init() {
    console.log('Connecting DB...');

    dbClient = await mongoose.connect(config.dburl, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
    app.locals.config = config;

    console.log('Loading Modules...');

    // logger
    app.use(morgan({
        format: 'short',
        stream: {
            write: (str) => {
                console.log(str);
            }
        }
    }));

    // routes
    app.use('/auth', require('./routes/auth'));
    app.use('/profile', require('./routes/profile'));
    app.use('/hear', require('./routes/hear'));
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
}

async function stopServer() {
    console.log('Stopping server');

    dbClient.close();
    httpServer.close();

    console.log('Stopped');
}

// process exit signal
process.on('SIGINT', function () {
    stopServer();
});

init();