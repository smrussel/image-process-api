# dominant color api endpoint response sample

dm_process_response = """
{
  "response": {
    "success": {
      "dominant_colors": [
        [
          0.23223333333333335,
          [
            134,
            171,
            194
          ]
        ],
        [
          0.22011666666666665,
          [
            235,
            219,
            211
          ]
        ],
        [
          0.21695,
          [
            80,
            104,
            128
          ]
        ],
        [
          0.17711666666666667,
          [
            36,
            142,
            176
          ]
        ],
        [
          0.15358333333333332,
          [
            38,
            53,
            69
          ]
        ]
      ],
      "output_image": "http://127.0.0.1:5000/images/77e4dd67-4349-4211-9d65-1e42ecd44859.png"
    }
  }
}
"""

# image background remove api endpoint response sample

bg_process_response = """
{
    "response": {
        "success": "http://127.0.0.1:5000/images/e12f7f3b-bcbc-4820-afd1-cfb281f124fb.png"
    }
}
"""

# image recognition api endpoint response sample

rg_process_response = """
{
    "response": {
        "success": {
            "result_one": [
                "Sports car",
                "0.883"
            ],
            "result_three": [
                [
                    "n04285008",
                    "sports_car",
                    "0.89931595"
                ],
                [
                    "n03100240",
                    "convertible",
                    "0.03339335"
                ],
                [
                    "n02974003",
                    "car_wheel",
                    "0.032635972"
                ],
                [
                    "n04037443",
                    "racer",
                    "0.029432505"
                ],
                [
                    "n03459775",
                    "grille",
                    "0.0030142132"
                ]
            ],
            "result_two": [
                "n04285008",
                "sports_car",
                "0.76035273"
            ]
        }
    }
}
"""