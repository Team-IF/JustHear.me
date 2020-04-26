const express = require("express");
const MongoClient = require('mongodb').MongoClient;
const config = require('./config/config');
const app = express();

async function init() {
    let dburl = `mongodb://${config.db.user}:${config.db.password}@${config.db.hostname}/${config.db.dbname}?authSource=admin&authMechanism=SCRAM-SHA-1`;
    let dbclient = new MongoClient(dburl, { useNewUrlParser: true });
    await dbclient.connect();
    let db = dbclient.db(config.db.dbname);

    app.use((req, res, next) => {
        console.log(`${req.connection.remoteAddress} : ${req.path}`);
        next();
    });

    app.use('/test', require('./routes/test')(db));

    //오류남
    //const router = require('./router/main')(app);

    const httpServer = app.listen(config.port, config.host, () => console.log(`Listening on port ${config.port}...`));
}

init();