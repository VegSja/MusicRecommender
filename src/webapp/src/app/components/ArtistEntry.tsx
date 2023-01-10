interface ArtistProps {
    name: String
}

function titleCase(str: String) {
   var splitStr = str.toLowerCase().split(' ');
   for (var i = 0; i < splitStr.length; i++) {
       // You do not need to check if i is larger than splitStr length, as your for does that for you
       // Assign it back to the array
       splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
   }
   // Directly return the joined string
   return splitStr.join(' '); 
}


export function ArtistEntry(props: ArtistProps) {
    


    return(
        <div className="bg-white inline-flex items-start dark:bg-gray-700 w-full rounded-md">
            <p className="text-slate-900 dark:text-white m-5 text-base font-medium tracking-tight">
                {titleCase(props.name)}
            </p>
        </div>
    )
}