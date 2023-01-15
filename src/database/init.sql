CREATE TABLE Artist(
    artist varchar(255) unique,
    spotifylink varchar(255),

    PRIMARY KEY (artist)
);

CREATE TABLE Playlist(
    PlaylistID int NOT NULL,
    Content TEXT,

    PRIMARY KEY (PlaylistID)
);

CREATE TABLE Rules(
    RuleID int NOT NULL,
    leftside varchar(255) NOT NULL,
    rightside varchar(255) NOT NULL,
    support FLOAT NOT NULL,

    PRIMARY KEY (RuleID),

    FOREIGN KEY (leftside) References Artist(artist),
    FOREIGN KEY (rightside) References Artist(artist)
);