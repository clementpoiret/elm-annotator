module Main exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)


view model =
    div [ class "jumbotron" ]
        [ h1 []
            [ text "Welcome to Dunder Mifflin"
            , a [ href "https://www.youtube.com/watch?v=dQw4w9WgXcQ" ] [ text "!" ]
            ]
        , p []
            [ text "Dunder Mifflin Inc. (stock symbol "
            , strong [] [ text "DMI" ]
            , text <|
                """
                ) is a micro-cap regional paper and office 
                supply distributor with an emphasis on servicing 
                small-business clients.
                """
            ]
        ]


main =
    view "dummy model"
