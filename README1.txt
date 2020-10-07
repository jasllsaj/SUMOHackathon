 Ideas so far:
- digital literacy
- helping vision impaired people pick items off shelves
    - segment and classification of items 


- indoor navigation (e.g. shopping centres, individual supermarkets)
    - incorporate computer vision to read off aisle numbers?
    - in-store map or something built off Google maps
    https://www.mapspeople.com/venues/retail/
    https://experienceinvestigators.com/how-in-store-navigation-impacts-customer-experience/

Importance of in-store navigation:
    - Retail stores are increasingly competing online shopping giants like Amazon
    - People will shop online if it is easier to do so
    - Elderly people, visually impaired people may also have a hard time reading store maps, wayfinding signage
    - elderly people may not be familiar with online shopping so don't have another alternative
    - smaller businesses without an online presence may also lose out if too many people favour bigger retailers with online stores
    - incentivise people to visit stores, increase foot traffic etc. to support retail jobs
    - retail industry has already taken a hit due to COVID-19 pandemic, online stores have seen a boom

Implementation:
    - Google Glass style
    - Tailored for individual stores: must download store data beforehand (or add user prompt upon entry)
    - integrated item search with store catalogue/stock levels

Modules to Develop:
- Audio/Speech to text and vice versa
    - speech input from user to determine the item they want
    - speech output to give directions
    - speech output to confirm whether item being picked up is correct
- Encoding store map data
    - bitmap implementation?
    - first bitmap to indicate aisle layout in the store
    - bitmap of each aisle to indicate where each item is (itemID)
        - if precisely locating item, then have a bitmap of each level too (assumed 3: top, middle, bottom shelves)
- Encoding store item locations
    - requires access to stock database
    - does not account for misplaced items
- Localisation
    - Apriltags (markers) placed around the store
    - Vision-based navigation?
    - Wi-Fi signals to triangulate user location
        - Can make use of Apple's Indoor Maps Program https://register.apple.com/resources/indoor/Apple-Indoor-Maps-Guidelines.pdf
- Store data query to locate the item
    - requires store database
- Path optimisation: determine the best way to get to said item
    - to do: find an algorithm to navigate to the right aisle
- Item detection: determine if the picked up item is correct
    - CV techniques