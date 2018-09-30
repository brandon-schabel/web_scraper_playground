import { gql } from 'apollo-boost'

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