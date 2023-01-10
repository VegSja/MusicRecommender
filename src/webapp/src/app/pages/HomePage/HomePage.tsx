
import axios from 'axios';
import * as React from 'react';
import { ArtistEntry } from '../../components/ArtistEntry';
import { InputField } from '../../components/inputfield';

export function HomePage() {
  const [recommendations, setRecommentations] = React.useState<string[]>(["Tom", "John", "Harry"])

  const onSearchSubmit = (query: String) => {
    axios.post("http://127.0.0.1:8000/recommend", {
      userID: "testUserId",
      artist: query
    }).then(res => {
      console.log(res)
      setRecommentations(res.data)
    })
  } 

  return (
  <div className='flex flex-col items-center w-full'>
      <h1 className='text-3xl font-bold dark:text-white text-center'>
        Artist recommendations
      </h1>
    <div className='w-1/2 mt-16'>
      <InputField onSubmit={onSearchSubmit}/>
      <div className="
        bg-white dark:bg-gray-700 
        inline-flex flex-col items-start 
        w-full rounded-md mt-5
        max-h-96
        overflow-y-scroll
        scrollbar scrollbar-thumb-gray-600 scrollbar-track-gray-700 scrollbar-small">
        {
          recommendations.map(rec => 
            <ArtistEntry name={rec} />
          )
        }
      </div>
    </div>
  </div>
  );
}