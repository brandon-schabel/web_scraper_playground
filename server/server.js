const express = require('express');
const graphqlHTTP = require('express-graphql')
const schema = require('./schema/schema')
const mongoose = require('mongoose')
const cors = require('cors')

const app = express();


const dbUrl = require('./secrets')
// allow cross-origin request
app.use(cors());

mongoose.connect(dbUrl);
mongoose.connection.once('open', () => {
  console.log('connected to databasee');
})

// when a request is made to '/graphql' it will know to let the graphqlHTTP package do the rest of the work
app.use('/graphql', graphqlHTTP({
  schema,
  graphiql: true // we want to use graphiql tool when we navigate to /graphql in browser
}));

app.listen(4000, () => {
  console.log('now listening on port 4000');
});