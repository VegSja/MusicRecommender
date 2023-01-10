interface ArtistProps {
    name: String
}

export function ArtistEntry(props: ArtistProps) {
    return(
        <div className="bg-white inline-flex items-start dark:bg-gray-700 w-full rounded-md">
            <p className="text-slate-900 dark:text-white m-5 text-base font-medium tracking-tight">
                {props.name}
            </p>
        </div>
    )
}