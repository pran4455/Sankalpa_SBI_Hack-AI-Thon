// Load third party dependencies
const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

// Load our custom classes
const CustomerStore = require('./customerStore.js');
const MessageRouter = require('./messageRouter.js');

// Grab the service account credentials path from an environment variable
const keyPath = process.env.DF_SERVICE_ACCOUNT_PATH;
if (!keyPath) {
    console.log('You need to specify a path to a service account keypair in environment variable DF_SERVICE_ACCOUNT_PATH. See README.md for details.');
    process.exit(1);
}

// Imports the Dialogflow client library
const dialogflow = require('@google-cloud/dialogflow').v2beta1;

// Instantiate a DialogFlow client.
const dialogflowClient = new dialogflow.SessionsClient({
    keyFilename: "./credentials.json"
});

const uuid = require('uuid');

// A unique identifier for the given session
const sessionId = uuid.v4();


// Grab the Dialogflow project ID from an environment variable
const projectId = process.env.DF_PROJECT_ID;
if (!projectId) {
    console.log('You need to specify a project ID in the environment variable DF_PROJECT_ID.');
    process.exit(1);
}

const sessionPath = dialogflowClient.projectAgentSessionPath(
    projectId,
    sessionId
);

// Instantiate our app
const customerStore = new CustomerStore();
const messageRouter = new MessageRouter({
    customerStore: customerStore,
    dialogflowClient: dialogflowClient,
    projectId: projectId,
    sessionPath: sessionPath,
    customerRoom: io.of('/customer'),
    operatorRoom: io.of('/operator')
});

// Serve static html files for the customer and operator clients
app.get('/customer', (req, res) => {
    res.sendFile(`${__dirname}/static/customer.html`);
});

app.get('/operator', (req, res) => {
    res.sendFile(`${__dirname}/static/operator.html`);
});

// Begin responding to websocket and http requests
messageRouter.handleConnections();
http.listen(3000, () => {
    console.log('Listening on *:3000');
});