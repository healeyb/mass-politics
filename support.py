import os
import json
import requests
import numpy as np
from database import Database

from openai import OpenAI
client = OpenAI()

from dotenv import load_dotenv
load_dotenv(override=True)

OTHER_CANDIDATE_ID = 9

def getMedian(data):
    try:
        data = np.array(data)
        dataMedian = np.median(data)

        return dataMedian

    except:
        logger.exception("Unable to compute median of values: %s", data)
        return None


class SupportService:
    def __init__(self):
        self.db = Database()

    def compose_language(self):
        output = {
            "senate": [],
            "house": []
        }

        # senate...

        sql = """SELECT senate_district_id, senate_primary_id, party, winner,
                     total_candidates, total_votes, other_votes
                 FROM senate_primaries
                 WHERE year = 2024;"""

        all_primaries = self.db.select_all(sql)

        sql = """SELECT c.candidate_id, c.name, c.party, c.ballotopedia_url,
                     spc.votes,  spc.senate_primary_id
                 FROM senate_primary_candidates spc 
                     JOIN candidates c ON (c.candidate_id = spc.candidate_id);"""

        all_primary_candidates = self.db.select_all(sql)

        sql = """SELECT senate_district_id, senate_election_id, winner,
                     total_primaries, uncontested_primaries, primary_votes,
                     total_candidates, total_votes, other_votes
                 FROM senate_elections
                 WHERE year = 2024;"""

        all_elections = self.db.select_all(sql)

        sql = """SELECT c.candidate_id, c.name, c.party, c.ballotopedia_url,
                     sec.votes, sec.senate_election_id
                 FROM senate_election_candidates sec 
                     JOIN candidates c ON (c.candidate_id = sec.candidate_id);"""

        all_election_candidates = self.db.select_all(sql)

        sql = """SELECT senate_district_id, name, ballotopedia_url
                 FROM senate_districts;"""

        senate_districts = self.db.select_all(sql)
        if senate_districts:
            for senate_district in senate_districts:
                senate_obj = {
                    "senate_district_id": senate_district["senate_district_id"],
                    "district": senate_district["name"],
                    "ballotpedia_url": senate_district["ballotopedia_url"],
                    "primaries": [],
                    "elections": [],
                }

                # get primaries...

                primaries = []
                for primary in all_primaries:
                    if primary["senate_district_id"] == senate_district["senate_district_id"]:
                        primaries.append(primary)

                if primaries:
                    for primary in primaries:
                        primary_obj = {
                            "senate_primary_id": primary["senate_primary_id"],
                            "party": primary["party"],
                            "metadata": {
                                "total_candidates": primary["total_candidates"],
                                "total_votes": primary["total_votes"],
                                "other_votes": primary["other_votes"],
                            },
                            "candidates": [],
                        }

                        candidates = []
                        for candidate in all_primary_candidates:
                            if candidate["senate_primary_id"] == primary["senate_primary_id"]:
                                candidates.append(candidate)

                        if candidates:
                            for candidate in candidates:
                                primary_obj["candidates"].append({
                                    "candidate_id": candidate["candidate_id"],
                                    "name": candidate["name"],
                                    "party": candidate["party"],
                                    "ballotpedia_url": candidate["ballotopedia_url"],
                                    "votes": candidate["votes"],
                                    "winner": True if candidate["candidate_id"] == primary["winner"] else False,
                                })

                        senate_obj["primaries"].append(primary_obj)

                # get elections...

                elections = []
                for election in all_elections:
                    if election["senate_district_id"] == senate_district["senate_district_id"]:
                        elections.append(election)

                if elections:
                    for election in elections:
                        election_obj = {
                            "senate_election_id": election["senate_election_id"],
                            "metadata": {
                                "total_primaries": election["total_primaries"],
                                "uncontested_primaries": election["uncontested_primaries"],
                                "primary_votes": election["primary_votes"],
                                "total_candidates": election["total_candidates"],
                                "total_votes": election["total_votes"],
                                "other_votes": election["other_votes"],
                            },
                            "candidates": [],
                        }

                        candidates = []
                        for candidate in all_election_candidates:
                            if candidate["senate_election_id"] == election["senate_election_id"]:
                                candidates.append(candidate)

                        if candidates:
                            for candidate in candidates:
                                election_obj["candidates"].append({
                                    "candidate_id": candidate["candidate_id"],
                                    "name": candidate["name"],
                                    "party": candidate["party"],
                                    "ballotpedia_url": candidate["ballotopedia_url"],
                                    "votes": candidate["votes"],
                                    "winner": True if candidate["candidate_id"] == election["winner"] else False,
                                })

                        senate_obj["elections"].append(election_obj)

                output["senate"].append(senate_obj)


        # house...

        sql = """SELECT house_district_id, house_primary_id, party, winner,
                     total_candidates, total_votes, other_votes
                 FROM house_primaries
                 WHERE year = 2024;"""

        all_primaries = self.db.select_all(sql)

        sql = """SELECT c.candidate_id, c.name, c.party, c.ballotopedia_url,
                     spc.votes,  spc.house_primary_id
                 FROM house_primary_candidates spc 
                     JOIN candidates c ON (c.candidate_id = spc.candidate_id);"""

        all_primary_candidates = self.db.select_all(sql)

        sql = """SELECT house_district_id, house_election_id, winner,
                     total_primaries, uncontested_primaries, primary_votes,
                     total_candidates, total_votes, other_votes
                 FROM house_elections
                 WHERE year = 2024;"""

        all_elections = self.db.select_all(sql)

        sql = """SELECT c.candidate_id, c.name, c.party, c.ballotopedia_url,
                     sec.votes, sec.house_election_id
                 FROM house_election_candidates sec 
                     JOIN candidates c ON (c.candidate_id = sec.candidate_id);"""

        all_election_candidates = self.db.select_all(sql)

        sql = """SELECT house_district_id, name, ballotopedia_url
                 FROM house_districts;"""

        house_districts = self.db.select_all(sql)
        if house_districts:
            for house_district in house_districts:
                house_obj = {
                    "house_district_id": house_district["house_district_id"],
                    "district": house_district["name"],
                    "ballotpedia_url": house_district["ballotopedia_url"],
                    "primaries": [],
                    "elections": [],
                }

                # get primaries...

                primaries = []
                for primary in all_primaries:
                    if primary["house_district_id"] == house_district["house_district_id"]:
                        primaries.append(primary)

                if primaries:
                    for primary in primaries:
                        primary_obj = {
                            "house_primary_id": primary["house_primary_id"],
                            "party": primary["party"],
                            "metadata": {
                                "total_candidates": primary["total_candidates"],
                                "total_votes": primary["total_votes"],
                                "other_votes": primary["other_votes"],
                            },
                            "candidates": [],
                        }

                        candidates = []
                        for candidate in all_primary_candidates:
                            if candidate["house_primary_id"] == primary["house_primary_id"]:
                                candidates.append(candidate)

                        if candidates:
                            for candidate in candidates:
                                primary_obj["candidates"].append({
                                    "candidate_id": candidate["candidate_id"],
                                    "name": candidate["name"],
                                    "party": candidate["party"],
                                    "ballotpedia_url": candidate["ballotopedia_url"],
                                    "votes": candidate["votes"],
                                    "winner": True if candidate["candidate_id"] == primary["winner"] else False,
                                })

                        house_obj["primaries"].append(primary_obj)

                # get elections...

                elections = []
                for election in all_elections:
                    if election["house_district_id"] == house_district["house_district_id"]:
                        elections.append(election)

                if elections:
                    for election in elections:
                        election_obj = {
                            "house_election_id": election["house_election_id"],
                            "metadata": {
                                "total_primaries": election["total_primaries"],
                                "uncontested_primaries": election["uncontested_primaries"],
                                "primary_votes": election["primary_votes"],
                                "total_candidates": election["total_candidates"],
                                "total_votes": election["total_votes"],
                                "other_votes": election["other_votes"],
                            },
                            "candidates": [],
                        }

                        candidates = []
                        for candidate in all_election_candidates:
                            if candidate["house_election_id"] == election["house_election_id"]:
                                candidates.append(candidate)

                        if candidates:
                            for candidate in candidates:
                                election_obj["candidates"].append({
                                    "candidate_id": candidate["candidate_id"],
                                    "name": candidate["name"],
                                    "party": candidate["party"],
                                    "ballotpedia_url": candidate["ballotopedia_url"],
                                    "votes": candidate["votes"],
                                    "winner": True if candidate["candidate_id"] == election["winner"] else False,
                                })

                        house_obj["elections"].append(election_obj)

                output["house"].append(house_obj)

        return output

    def calculate_primary_stats(self, primary_id, primary_type="senate"):
        if primary_type == "senate":
            sql = """SELECT candidate_id, votes
                     FROM senate_primary_candidates
                     WHERE senate_primary_id = %s;"""

        elif primary_type == "house":
            sql = """SELECT candidate_id, votes
                     FROM house_primary_candidates
                     WHERE house_primary_id = %s;"""

        candidate_count = 0
        vote_count = 0
        other_votes = 0

        candidates = self.db.select_all(sql, (primary_id,))
        for candidate in candidates:
            if candidate["candidate_id"] == OTHER_CANDIDATE_ID:
                other_votes += candidate["votes"]

            else:
                candidate_count += 1
                vote_count += candidate["votes"]

        if primary_type == "senate":
            sql = """UPDATE senate_primaries
                     SET total_candidates = %s, 
                         total_votes = %s,
                         other_votes = %s
                     WHERE senate_primary_id = %s;"""

        elif primary_type == "house":
            sql = """UPDATE house_primaries
                     SET total_candidates = %s, 
                         total_votes = %s,
                         other_votes = %s
                     WHERE house_primary_id = %s;"""

        self.db.mutate(sql, (candidate_count, vote_count, other_votes, primary_id))

        return candidate_count, vote_count

    def calculate_election_stats(self, election_id, election_type="senate"):
        if election_type == "senate":
            sql = """SELECT candidate_id, votes
                     FROM senate_election_candidates
                     WHERE senate_election_id = %s;"""

        elif election_type == "house":
            sql = """SELECT candidate_id, votes
                     FROM house_election_candidates
                     WHERE house_election_id = %s;"""

        candidate_count = 0
        vote_count = 0
        other_votes = 0

        candidates = self.db.select_all(sql, (election_id,))
        for candidate in candidates:
            if candidate["candidate_id"] == OTHER_CANDIDATE_ID:
                other_votes += candidate["votes"]

            else:
                candidate_count += 1
                vote_count += candidate["votes"]

        if election_type == "senate":
            sql = """UPDATE senate_elections
                     SET total_candidates = %s, 
                         total_votes = %s,
                         other_votes = %s
                     WHERE senate_election_id = %s;"""

        elif election_type == "house":
            sql = """UPDATE house_elections
                     SET total_candidates = %s, 
                         total_votes = %s,
                         other_votes = %s
                     WHERE house_election_id = %s;"""

        self.db.mutate(sql, (candidate_count, vote_count, other_votes, election_id))

        return candidate_count, vote_count

    def create_senate_stats(self, ref_year=2024):
        sql = """SELECT senate_district_id
                 FROM senate_districts
                 ORDER BY senate_district_id ASC;"""

        by_district = {}
        overall = {
            "dual_uncontested": 0,
            "uncontested_primaries": 0,
            "uncontested_elections": 0,
        }

        for district in self.db.select_all(sql):
            sql = """SELECT senate_primary_id
                     FROM senate_primaries
                     WHERE senate_district_id = %s AND 
                        year = %s AND
                        winner IS NOT NULL;"""

            total_primaries = 0
            uncontested_primaries = 0
            uncontested_votes = 0
            contested_primaries = 0
            contested_votes = 0
            primary_votes = 0

            for primary in self.db.select_all(sql, (district["senate_district_id"], ref_year,)):
                total_primaries += 1
                candidate_count, vote_count = self.calculate_primary_stats(
                    primary_id=primary["senate_primary_id"],
                    primary_type="senate",
                )

                primary_votes += vote_count
                if candidate_count == 1:
                    uncontested_primaries += 1
                    uncontested_votes += vote_count
                else:
                    contested_primaries += 1
                    contested_votes += vote_count

            by_district[district["senate_district_id"]] = {
                "primaries": {
                    "total": total_primaries,
                    "primary_votes": primary_votes,
                    "uncontested": uncontested_primaries,
                    "uncontested_votes": uncontested_votes,
                    "contested": contested_primaries,
                    "contested_votes": contested_votes,
                }
            }

            sql = """SELECT senate_election_id
                     FROM senate_elections
                     WHERE senate_district_id = %s AND 
                        year = %s AND
                        winner IS NOT NULL;"""

            election = self.db.select_one(sql, (district["senate_district_id"], ref_year,))
            if election:
                sql = """UPDATE senate_elections
                         SET total_primaries = %s,
                             uncontested_primaries = %s,
                             primary_votes = %s
                         WHERE senate_election_id = %s;"""

                self.db.mutate(sql, (total_primaries, uncontested_primaries, primary_votes, election["senate_election_id"]))

                candidate_count, vote_count = self.calculate_election_stats(
                    election_id=election["senate_election_id"],
                    election_type="senate",
                )

                if candidate_count == 1:
                    by_district[district["senate_district_id"]]["election"] = {
                        "uncontested": True,
                        "contested": False,
                        "votes": vote_count,
                    }

                else:
                    by_district[district["senate_district_id"]]["election"] = {
                        "uncontested": False,
                        "contested": True,
                        "votes": vote_count,
                    }

                if by_district[district["senate_district_id"]]["primaries"]["contested"] == 0:
                    overall["uncontested_primaries"] += 1

                if by_district[district["senate_district_id"]]["election"]["uncontested"]:
                    overall["uncontested_elections"] += 1
                    if by_district[district["senate_district_id"]]["primaries"]["contested"] == 0:
                        overall["dual_uncontested"] += 1

        # TODO: do something with by_distict?

        sql = """INSERT INTO senate_election_stats
                 (year, stats) VALUES (%s, %s)
                 ON DUPLICATE KEY UPDATE stats = VALUES(stats);"""

        self.db.insert(sql, (2024, json.dumps(overall)))

    def create_house_stats(self, ref_year=2024):
        sql = """SELECT house_district_id
                 FROM house_districts
                 ORDER BY house_district_id ASC;"""

        by_district = {}
        overall = {
            "dual_uncontested": 0,
            "uncontested_primaries": 0,
            "uncontested_elections": 0,
        }

        for district in self.db.select_all(sql):
            sql = """SELECT house_primary_id
                     FROM house_primaries
                     WHERE house_district_id = %s AND 
                        year = %s AND
                        winner IS NOT NULL;"""

            total_primaries = 0
            uncontested_primaries = 0
            uncontested_votes = 0
            contested_primaries = 0
            contested_votes = 0
            primary_votes = 0

            for primary in self.db.select_all(sql, (district["house_district_id"], ref_year,)):
                total_primaries += 1
                candidate_count, vote_count = self.calculate_primary_stats(
                    primary_id=primary["house_primary_id"],
                    primary_type="house",
                )

                primary_votes += vote_count
                if candidate_count == 1:
                    uncontested_primaries += 1
                    uncontested_votes += vote_count
                else:
                    contested_primaries += 1
                    contested_votes += vote_count

            by_district[district["house_district_id"]] = {
                "primaries": {
                    "total": total_primaries,
                    "primary_votes": primary_votes,
                    "uncontested": uncontested_primaries,
                    "uncontested_votes": uncontested_votes,
                    "contested": contested_primaries,
                    "contested_votes": contested_votes,
                }
            }

            sql = """SELECT house_election_id
                     FROM house_elections
                     WHERE house_district_id = %s AND 
                        year = %s AND
                        winner IS NOT NULL;"""

            election = self.db.select_one(sql, (district["house_district_id"], ref_year,))
            if election:
                sql = """UPDATE house_elections
                         SET total_primaries = %s,
                             uncontested_primaries = %s,
                             primary_votes = %s
                         WHERE house_election_id = %s;"""

                self.db.mutate(sql,
                               (total_primaries, uncontested_primaries, primary_votes, election["house_election_id"]))

                candidate_count, vote_count = self.calculate_election_stats(
                    election_id=election["house_election_id"],
                    election_type="house",
                )

                if candidate_count == 1:
                    by_district[district["house_district_id"]]["election"] = {
                        "uncontested": True,
                        "contested": False,
                        "votes": vote_count,
                    }

                else:
                    by_district[district["house_district_id"]]["election"] = {
                        "uncontested": False,
                        "contested": True,
                        "votes": vote_count,
                    }

                if by_district[district["house_district_id"]]["primaries"]["contested"] == 0:
                    overall["uncontested_primaries"] += 1

                if by_district[district["house_district_id"]]["election"]["uncontested"]:
                    overall["uncontested_elections"] += 1
                    if by_district[district["house_district_id"]]["primaries"]["contested"] == 0:
                        overall["dual_uncontested"] += 1

        # TODO: do something with by_distict?

        sql = """INSERT INTO house_election_stats
                 (year, stats) VALUES (%s, %s)
                 ON DUPLICATE KEY UPDATE stats = VALUES(stats);"""

        self.db.insert(sql, (2024, json.dumps(overall)))

    def get_avgs(self):
        uncontested_votes = []
        contested_votes = []

        sql = """SELECT total_votes
                 FROM senate_elections
                 WHERE year = 2024 
                    AND total_candidates = 1
                    AND total_primaries = 1
                    AND uncontested_primaries = 1;"""

        for votes in self.db.select_all(sql):
            uncontested_votes.append(votes["total_votes"])

        uncontested_votes = getMedian(uncontested_votes)
        print(f"Senate Uncontested: {uncontested_votes}")

        sql = """SELECT total_votes
                 FROM senate_elections
                 WHERE year = 2024 
                    AND total_candidates > 1;"""

        for votes in self.db.select_all(sql):
            contested_votes.append(votes["total_votes"])

        contested_votes = getMedian(contested_votes)
        print(f"Senate Contested: {contested_votes}")

        # House...

        uncontested_votes = []
        contested_votes = []

        sql = """SELECT total_votes
                 FROM house_elections
                 WHERE year = 2024 
                    AND total_candidates = 1
                    AND total_primaries = 1
                    AND uncontested_primaries = 1;"""

        for votes in self.db.select_all(sql):
            uncontested_votes.append(votes["total_votes"])

        uncontested_votes = getMedian(uncontested_votes)
        print(f"House Uncontested: {uncontested_votes}")

        sql = """SELECT total_votes
                 FROM house_elections
                 WHERE year = 2024 
                    AND total_candidates > 1;"""

        for votes in self.db.select_all(sql):
            contested_votes.append(votes["total_votes"])

        contested_votes = getMedian(contested_votes)
        print(f"House Contested: {contested_votes}")

