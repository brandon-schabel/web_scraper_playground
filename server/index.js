const express = require('express');
const graphqlHTTP = require('express-graphql')
const mongoose = require('mongoose')
const cors = require('cors')
const Profile = require('./models/profile');
const { buildSchema } = require('graphql')

require('dotenv').config();


const schema = buildSchema(`
  type Profile {
    id: String
    name: String
    reason: String
    image_url: String
    liked: String
    age: Int
    datetime: String
  }

  type Query {
    profile(id: String): Profile
    profiles: [Profile]
  }
`)

const root = {
  profile:  ({id}) => {
    return Profile.findById(mongoose.Types.ObjectId(id));
  },
  profiles: () => {
  
    return Profile.find({});
  }
};



const app = express();

// allow cross-origin request
app.use(cors());

app.post('/delete', function(req, res, next) {
  //console.log(req);
  //console.log(req.headers)
  let id = req.headers.id

  /*
  Profile.deleteOne({id: id}, (err, res)=> {
    if(err) return handleError(err);
    console.log(res)
  }) */
  let response = {}
  Profile.findByIdAndDelete(id,(err,res)=> {
    if(err){
      res.status(500).send(err)
    }

    console.log(id + " successfully deleted")
    response = {
      message: id + "successfully deleted"
    }
  })
  res.status(200).send(response);

});

mongoose.connect(process.env.DB_URL);
mongoose.connection.once('open', () => {
  console.log('connected to database');
})

// when a request is made to '/graphql' it will know to let the graphqlHTTP package do the rest of the work
app.use('/graphql', graphqlHTTP({
  schema,
  rootValue: root,
  graphiql: true // we want to use graphiql tool when we navigate to /graphql in browser
}));

app.listen(4000, () => {
  console.log('now listening on port 4000');
});