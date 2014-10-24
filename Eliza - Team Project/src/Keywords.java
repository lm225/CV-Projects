import java.io.*;
import java.util.Random;

public class Keywords {

	public boolean findKeywords(String[] words) throws IOException{

		boolean output = false;
		try{
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String keywords;

			//read each line of the script (to the end)
			while ((keywords = reader.readLine()) != null) {
				//check that the first character of the line is a 2
				for(int i = 0; i < words.length; i ++){
					if (keywords.charAt(0) == ('2')) {
						//array to contain the words of each line in the script
						String[] response = keywords.split("::");

						//check that the current word array element is equal to the second response array element
						if (words[i].equals(response[1])) {


							//generate a random number to give a random response
							int r = 0;
							while(r < 2){
								Random random = new Random();
								r = random.nextInt(response.length);
							}						
							System.out.println(response[r]);
							output = true;
							return output;


						}
					}
				}


			}
		}
		catch(FileNotFoundException e){
			System.out.println("The File Specified Could Not Be Found");
		}

		return output;
	}



}
