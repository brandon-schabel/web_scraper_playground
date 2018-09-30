const Profile = require('../models/profile');
const { buildSchema } = require('graphql')

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

module.exports = {
  query: root,
  schema: schema
};
