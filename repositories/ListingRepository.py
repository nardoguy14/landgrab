from repositories.BaseRepository import BaseRepository


class ListingRepository:
    def create_listing(self, listing):
        with BaseRepository() as base_repo:
            sql = """
            INSERT INTO listings (
                address,
                cost,
                beds,
                baths,
                rating_url,
                rentometer_url,
                zillow_url,
                cashOnCashReturn,
                percentageReturn,
                rating,
                cashflow,
                monthly_cost,
                rent    
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                listing['info']['address'],
                listing['info']['cost'],
                int(listing['info']['numberOfBeds']),
                int(listing['info']['numberOfBaths']),
                listing['links']['rating'],
                listing['links']['rentometer'],
                listing['links']['zillow'],
                listing['stats']['%']['cashOnCashReturn'],
                listing['stats']['%']['percentageReturn'],
                listing['stats']['rating'],
                float(listing['stats']['raw']['cashflow']),
                float(listing['stats']['raw']['monthlyCost']),
                float(listing['stats']['raw']['rentalValue']),
            )

            base_repo.execute(sql, val)
            return base_repo.lastrowid


    def get_listing(self, address):
        with BaseRepository() as base_repo:
            query = (f"""SELECT 
                            id
                        FROM listings 
                        WHERE address = %s
                    """)
            params = [address]
            filtered_params = tuple(list(filter(lambda x: x != None, params)))
            base_repo.execute(query, filtered_params)

            results = []
            for (
                    id,
            ) in base_repo:
                results.append(id)

            return results