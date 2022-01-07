import os
import json, requests, argparse
import datetime



def api_call(gitUser):
    GIST_URL = 'http://api.github.com/users/' + gitUser + '/gists'
    r = requests.get(GIST_URL)
    if (r.status_code != 200):
        if (r.status_code == 404):
            print(f"GitHub user {gitUser} does not exist")
        else:
            r.raise_for_status()
    else:
        gist_data = r.json()
        if not gist_data:
            print('Github user "' + gitUser + '" has not published any gists.')
            exit(1)
    return gist_data

def check_if_file_exist(filename):
    if not os.path.isfile(filename):
        return False
    else:
        return True
def process_data(user):
    gist_data = api_call(user)
    latest_gist = {}
    if check_if_file_exist("data.json"):
        try:
            f = open('data.json', 'r')
            data = json.load(f)
        except Exception as e:
            raise

        lastCreateDate = datetime.datetime.strptime(data['latestGist']['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        currentCreateDate = datetime.datetime.strptime(gist_data[0]['created_at'],
                                                       '%Y-%m-%dT%H:%M:%SZ')

        if currentCreateDate > lastCreateDate:
            newGist = []
            print('Github user "' + user + '" created a new gist since the last query.')
            latest_gist["latestGist"] = gist_data[0]
            for gist in gist_data:
                created_date = datetime.datetime.strptime(gist['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if (created_date > lastCreateDate):
                    newGist.append(gist)
            print("newly created gists are", newGist)

            try:
                with open('data.json', 'w') as f:
                    f.write(json.dumps(latest_gist))
                    f.close()
            except Exception as e:
                raise
        else:
            print('Github user "' + user + '" has not created a new gist since the last query.')
    else:
        print("there is no file available, hence this is first run")
        latest_gist["latestGist"] = gist_data[0]
        print(gist_data)
        try:
            with open('data.json', 'w') as f:
                f.write(json.dumps(latest_gist))
                f.close()
        except Exception as e:
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-gitUser", help="Github username for gists query")
    args = parser.parse_args()
    process_data(args.gitUser)

