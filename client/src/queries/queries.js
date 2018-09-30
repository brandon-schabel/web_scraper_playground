import { gql } from 'apollo-boost'



export const getProfileQuery = `
  query($id: ID) {
    profile(id: $id) {
      id
      name
      reason
      image_url
      liked
      age
    }
  }
`
export const getProfilesQuery = gql`
  {
    profiles{
      id
      name
      reason
      image_url
      liked
      age
    }
  }
`