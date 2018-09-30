const graphql = require('graphql');
const _ = require('lodash');
const Profile = require('../models/profile');

// below we destructor "GraphQLObjectType" from graphql package  to use it as var/function
const { GraphQLObjectType, 
        GraphQLInt,
        GraphQLString, 
        GraphQLSchema,
        GraphQLID,
        GraphQLList,
        GraphQLNonNull, 
        GraphQLInputObjectType
      } = graphql;


const ProfileType = new GraphQLObjectType({
  name: 'Profile', // our 'Book' type schema
  fields: () => ({ 
    id: { type: GraphQLID },
    name: { type: GraphQLString },
    reason: { type: GraphQLString},
    image_url: {type: GraphQLString},
    liked: { type: GraphQLString},
    age: { type: GraphQLInt},
    //attributes: {type: Ouput}
  })
});

/*
{
  smile: {type: GraphQLInt},
  gender: {type: GraphQLString},
  hair: [
    {color: {type: GraphQLString}},
    {confidence: {type: GraphQLInt}}
  ]
} */

const RootQuery = new GraphQLObjectType({
  name: 'RootQueryType',
  fields: {
    profile: {
      type: ProfileType,
      // when they query for a book type we expect a set of args
      args: { id: { type: GraphQLID } },
      resolve(parent, args) {
        //code to get data from db / other source
        // below we use lodash to find any books with id passed from args.id
        return Profile.findById(args.id);
      }
    },

    // root queries that tell graphql that we want can retrieve all authors and all books
    profiles: {
      type: new GraphQLList(ProfileType),
      resolve(parent, args) {
        return Profile.find({})
      }
    },
  }
});

module.exports = new GraphQLSchema({
  query: RootQuery,
  // mutation: Mutation
});
//the export is saying we can query using RootQuery and use mutations defined in Mutation