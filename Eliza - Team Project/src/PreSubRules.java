import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

public class PreSubRules {

	public boolean preSubRule(String[] words) throws IOException{

		boolean output = false;
		PostSubRules post = new PostSubRules();
		try{
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String keywords;


			for(int i = 0; i < words.length; i ++){
				//read each line of the script (to the end)
				while ((keywords = reader.readLine()) != null) {
					//check that the first character of the line is a 0
					if (keywords.charAt(0) == ('0')) {
						//array to contain the words of each line in the script
						String[] response = keywords.split("::");
						//check that the current word array element equals the second response array element
						if (words[i].equals(response[1])) {
							output = true;
							//replace the current word element with the new element in the array
							words[i] = response[2];
							//call the post-substitution method on the new element
							post.postSubRules(words, i);
							Keywords k = new Keywords();
							k.findKeywords(words);

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
