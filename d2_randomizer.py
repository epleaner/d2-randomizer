import pandas, json, random, argparse, os
from name_generator import NameGenerator

def read_uniques():
  unique_items_txt = r"UniqueItems.txt"

  if not os.path.isfile(unique_items_txt):
    print "Please have UniqueItems.txt in the working directory."
    sys.exit()

  df = pandas.read_csv(unique_items_txt,index_col=False, delimiter="\t", dtype=str)

  return df

def load_props():
  with open("all_props") as f:
    props = json.load(f)

  return props

def write_uniques(df):
  randomized_unique_items_txt = r"UniqueItems_randomized.txt"
  df.to_csv(path_or_buf=randomized_unique_items_txt, index=False, sep="\t", line_terminator="\r\n")

  print "Wrote new uniques to " + randomized_unique_items_txt

def get_item_bucket(lvl):
  lvl_buckets = [[0, 36], [36, 73], [73, 110]]
  item_bucket = 0
  for i,bucket in enumerate(lvl_buckets):
      if lvl in range(*bucket):
          item_bucket = i
  return item_bucket

def bucket(mn,mx):
    
    buckets=[]
    for c in pandas.cut([mn,mx],3).categories:
        l,w = c.split(', ')
        l,w = int(float(l[1:])),int(float(w[:-1]))
        buckets.append([l,w])
    
    return buckets

def get_random_props(num_props, all_props, item_bucket, balance):
    props = []
    for i in range(0, num_props):
        new_prop_key = random.choice(all_props.keys())
        new_prop = {"prop": new_prop_key, "par": "null", "min": "null", "max": "null"}

        if "boolean_prop" in all_props[new_prop_key]:
            new_prop["min"] = 1
            new_prop["max"] = 1
            
        else:
            if "min" in all_props[new_prop_key] and "max" in all_props[new_prop_key]:
                prop_min = all_props[new_prop_key]["min"]
                prop_max = all_props[new_prop_key]["max"]
                
                bucket_min, bucket_max = prop_min, prop_max

                if balance:
                  bucket_min, bucket_max = bucket(prop_min,prop_max)[item_bucket]
   
                rand_1 = random.randint(bucket_min, bucket_max)
                rand_2 = random.randint(bucket_min, bucket_max)

                new_prop["min"] = rand_1 if rand_1 < rand_2 else rand_2
                new_prop["max"] = rand_1 if rand_1 > rand_2 else rand_2
                
            if "possible_values" in all_props[new_prop_key]:
                rand_value = random.choice(all_props[new_prop_key]["possible_values"])
                new_prop["par"] = rand_value
        props.append(new_prop)
    return props

def randomize(balance=True, randomize_names=False):
  name_gen = NameGenerator()
  all_props = load_props();
  df = read_uniques()

  print "Randomizing..."

  for i, row in df.iterrows():

    lvl = df.at[i, "lvl"]
    lvl = 0 if pandas.isnull(lvl) else int(lvl)

    item_bucket = get_item_bucket(lvl)

    if randomize_names:
      df.at[i, "index"] = name_gen.rand_name()

    prop_cols = ["prop" + `ix` for ix in range(1,13)] 
    num_props = len([r for r in row[prop_cols] if type(r) is str])
    random_props = get_random_props(num_props, all_props, item_bucket, balance)
    for prop_ndx, prop in enumerate(random_props):
        df.at[i, "prop" + `prop_ndx + 1`] = prop["prop"]
        df.at[i, "par" + `prop_ndx + 1`] = prop["par"] if prop["par"] != "null" else ""
        df.at[i, "min" + `prop_ndx + 1`] = str(prop["min"]) if prop["min"] != "null" else ""
        df.at[i, "max" + `prop_ndx + 1`] = str(prop["max"]) if prop["max"] != "null" else ""

  write_uniques(df)

if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(description='Randomize Diablo II Unique Items')
    parser.add_argument('--no-balance', help="Do not balance attributes for item level (will balance by default)", dest='no_balance', default=False, action='store_true')
    args = parser.parse_args()

    balance = not args.no_balance

    randomize(balance)